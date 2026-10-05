"""Standard-library orchestration; no original econometric code is included."""
import argparse
import csv
import hashlib
import json
import math
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def rows(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def local(root, name):
    p = (root / name).resolve()
    if not p.is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes repository: {name}')
    return p


def validate(root):
    stages = json.loads((root / 'config/pipeline.json').read_text())['stages']
    spec = json.loads((root / 'config/study_spec.json').read_text())
    if not stages or not isinstance(spec, dict) or not spec:
        raise ValueError('Empty stages or study specification')
    manifest = rows(root / 'config/data_manifest.csv')
    if not manifest:
        raise ValueError('Empty input manifest')
    available = {'config/output_manifest.csv', 'config/study_spec.json'}
    for row in manifest:
        local(root, row['path'])
        if row['path'] in available or row['required'] not in ('true', 'false'):
            raise ValueError('Duplicate input or invalid required flag')
        available.add(row['path'])
    ids, outputs = set(), set()
    for s in stages:
        if not re.fullmatch(r'[0-9]{2}_[a-z0-9_]+', s['id']) or s['id'] in ids:
            raise ValueError('Invalid or duplicate stage ID')
        ids.add(s['id'])
        if not isinstance(s['implemented'], bool):
            raise ValueError('implemented must be boolean')
        if not isinstance(s['command'], list) or not s['command'] or not all(isinstance(x, str) and x for x in s['command']):
            raise ValueError('command must be an argv list')
        for key in ('inputs', 'outputs'):
            if not isinstance(s[key], list) or not s[key]:
                raise ValueError(f'Empty {key}')
            for name in s[key]:
                local(root, name)
        for name in s['inputs']:
            if name not in available:
                raise ValueError(f'Input has no earlier producer/manifest: {name}')
        for name in s['outputs']:
            if name in outputs or name in available or name.startswith(('data/raw/', 'config/', 'src/', 'benchmarks/')):
                raise ValueError(f'Invalid output: {name}')
            outputs.add(name)
        available.update(s['outputs'])
    rows(root / 'config/output_manifest.csv')
    return stages


def readiness(root, stages):
    errors = []
    spec = json.loads((root / 'config/study_spec.json').read_text())
    for key, value in spec.items():
        if value is None or value == '' or value == [] or value == {}:
            errors.append(f'Unresolved study specification: {key}')
    for row in rows(root / 'config/data_manifest.csv'):
        path = local(root, row['path'])
        if row['required'] == 'false' and not path.exists():
            continue
        for field in ('source_url', 'upstream_filename', 'release_or_extract_id', 'access_instructions', 'license_or_terms'):
            if not row.get(field):
                errors.append(f'{row["dataset_id"]}: missing {field}')
        if not re.fullmatch(r'[a-fA-F0-9]{64}', row.get('sha256', '')):
            errors.append(f'{row["dataset_id"]}: missing/invalid SHA-256')
        if not path.is_file():
            errors.append(f'Missing input: {row["path"]}')
        elif row.get('sha256') and sha256(path) != row['sha256'].lower():
            errors.append(f'Checksum mismatch: {row["path"]}')
    for s in stages:
        if not s['implemented']:
            errors.append(f'Original code not integrated: {s["id"]}')
    mapped = rows(root / 'config/output_manifest.csv')
    if not mapped:
        errors.append('Output manifest is empty; supply original benchmarks')
    seen = set()
    for row in mapped:
        for field in ('output_id', 'manuscript_item', 'path', 'stage_id', 'benchmark_path', 'validation_rule'):
            if not row.get(field):
                errors.append(f'Output mapping missing {field}')
        if row.get('output_id') in seen:
            errors.append('Duplicate output_id')
        seen.add(row.get('output_id'))
        producer = next((s for s in stages if s['id'] == row.get('stage_id')), None)
        if not producer or row.get('path') not in producer['outputs']:
            errors.append(f'Output not declared by stage: {row.get("path")}')
        if row.get('benchmark_path') and not local(root, row['benchmark_path']).is_file():
            errors.append(f'Missing benchmark: {row["benchmark_path"]}')
        for key in ('atol', 'rtol'):
            if row.get(key):
                try:
                    number = float(row[key])
                    if number < 0 or not math.isfinite(number):
                        raise ValueError
                except ValueError:
                    errors.append(f'Invalid {key}')
    return errors


def run_stage(root, stage, log_dir):
    for name in stage['inputs']:
        if not local(root, name).is_file():
            raise RuntimeError(f'Missing stage input: {name}')
    for name in stage['outputs']:
        p = local(root, name)
        if p.exists():
            raise RuntimeError(f'Output already exists; archive/remove generated file: {name}')
        p.parent.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable if x == '{python}' else x for x in stage['command']]
    log = log_dir / (stage['id'] + '.log')
    with log.open('w', encoding='utf-8') as f:
        result = subprocess.run(cmd, cwd=root, stdout=f, stderr=subprocess.STDOUT, check=False)
    if result.returncode:
        raise RuntimeError(f'{stage["id"]} failed ({result.returncode}); see {log}')
    for name in stage['outputs']:
        if not local(root, name).is_file():
            raise RuntimeError(f'Declared output not created: {name}')


def run(root, stages):
    problems = readiness(root, stages)
    if problems:
        raise RuntimeError('Preflight blocked:\n- ' + '\n- '.join(problems))
    existing = [p for s in stages for p in s['outputs'] if local(root, p).exists()]
    if existing:
        raise RuntimeError('Archive/remove generated outputs before a clean run:\n- ' + '\n- '.join(existing))
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    logs = root / 'logs' / stamp
    logs.mkdir(parents=True)
    for stage in stages:
        print('Running ' + stage['id'], flush=True)
        run_stage(root, stage, logs)
    def git(*args):
        try:
            return subprocess.check_output(['git', *args], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()
        except (OSError, subprocess.CalledProcessError):
            return 'unavailable'
    files = [p for s in stages for p in s['outputs']]
    files += [r['path'] for r in rows(root / 'config/data_manifest.csv') if local(root, r['path']).is_file()]
    files += ['config/' + p for p in ('pipeline.json', 'study_spec.json', 'data_manifest.csv', 'output_manifest.csv')]
    record = dict(status='completed_declared_pipeline', utc_completed=datetime.now(timezone.utc).isoformat(),
                  python=sys.version, platform=platform.platform(), commit=git('rev-parse', 'HEAD'),
                  git_status=git('status', '--porcelain'), stages=stages,
                  sha256={p: sha256(local(root, p)) for p in files})
    (logs / 'run_manifest.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print(f'Completed declared pipeline. Inspect benchmark comparison and {logs}/run_manifest.json')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    for arg in ('validate-scaffold', 'dry-run', 'check', 'run'):
        group.add_argument('--' + arg, action='store_true')
    group.add_argument('--hash', metavar='FILE')
    args = parser.parse_args()
    try:
        if args.hash:
            print(sha256(local(ROOT, args.hash)))
            return 0
        stages = validate(ROOT)
        if args.validate_scaffold:
            print('Scaffold structure valid; empirical replication is not validated.')
        elif args.dry_run:
            for s in stages:
                print(f'{s["id"]}: {json.dumps(s["command"])}; implemented={s["implemented"]}')
                print(f'  inputs={s["inputs"]}\n  outputs={s["outputs"]}')
        elif args.check:
            errors = readiness(ROOT, stages)
            if errors:
                print('NOT READY:\n- ' + '\n- '.join(errors))
                return 1
            print('Preflight checks passed; run and benchmark validation still required.')
        else:
            run(ROOT, stages)
        return 0
    except (ValueError, KeyError, TypeError, OSError, RuntimeError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
