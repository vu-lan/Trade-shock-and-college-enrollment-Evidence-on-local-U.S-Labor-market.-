# Checklist bàn giao của Lan

**Hiện trạng:** đã có khung tổ chức và bộ điều phối; chưa có dữ liệu, code phân tích hoặc kết quả chuẩn. Không đánh dấu “replication-ready” trước khi người khác chạy lại thành công. Tên file dưới đây là tên đề xuất, không phải tên file đã được xác nhận.

| Ưu tiên | Tệp/gói Lan cần bổ sung | Đặt ở đâu / điều kiện hoàn thành |
|---|---|---|
| P0 | Bản luận văn/bài viết đúng phiên bản kết quả cần tái lập, phụ lục, danh mục bảng/hình | Ghi phiên bản và link truy cập trong README; chỉ đưa PDF lên nếu muốn công khai |
| P0 | Toàn bộ code gốc: master + script import/clean/merge/ước lượng/xuất kết quả và hàm/ado tự viết | `src/`; giữ bản gốc để đối chiếu, nối vào 7 stage; không chỉ gửi đoạn hồi quy cuối |
| P0 | Mỗi extract vi dữ liệu gốc + XML/DDI/codebook + syntax đọc dữ liệu | `data/raw/`; cập nhật manifest theo đúng số file/năm; nếu hạn chế chia sẻ, bổ sung cách người dùng tự xin/tải |
| P0 | Cấu hình extract: năm/sample, universe, biến chọn, extract ID, ngày tải | `docs/DATA_ACCESS.md` và metadata công khai được phép chia sẻ |
| P0 | File crosswalk đúng vintage + tài liệu trọng số phân bổ | `data/raw/`; chỉ rõ mã bang/PUMA/CZ, cardinality và xử lý phần không match |
| P0 | File ADH đã dùng, chứa exposure/IV; hoặc toàn bộ trade/employment/concordance/deflator nếu tự dựng | `data/raw/`; chọn đúng một nhánh theo code gốc, không mặc định cần cả hai |
| P0 | Các nguồn controls/biến cơ chế khác thực sự dùng | Thêm từng file và checksum vào `config/data_manifest.csv` |
| P0 | Đặc tả chính xác của mẫu, outcome, treatment, IV, controls, FE, weights, SE | Điền mọi `null` trong `config/study_spec.json`; hoàn thiện `docs/VARIABLES.md` và `docs/METHODOLOGY.md` |
| P0 | Kết quả gốc chưa làm tròn: hệ số, SE, N, first stage; bảng/hình chuẩn | `benchmarks/reference_metrics.csv` (output_id, metric, expected); ánh xạ đầy đủ trong `config/output_manifest.csv` |
| P0 | Danh sách phần mềm và dependencies thực sự đã chạy | `docs/SOFTWARE.md`; bổ sung lockfile đã kiểm chứng; không coi requirements hiện tại là môi trường mô hình |
| P1 | Mã kiểm tra dữ liệu và so khớp kết quả chuẩn | Tích hợp vào từng stage và stage 07; sai tolerance phải trả exit code khác 0 |
| P1 | Thời gian chạy, RAM/disk, phiên bản OS/phần mềm, log lần chạy sạch | Đo thực tế và ghi lại; log không chứa dữ liệu cá nhân |
| P1 | Quyết định license code, điều khoản từng bộ dữ liệu và thông tin trích dẫn | Thêm LICENSE/CITATION sau khi xác nhận, không gán license cho dữ liệu bên thứ ba |
| P1 | Biên bản người khác chạy từ clone sạch | Ghi commit, cách lấy input, checksum, môi trường và kết quả so sánh |

## Thứ tự bàn giao nhanh nhất

1. Gửi manuscript + toàn bộ code gốc + log/kết quả gốc để chốt mô hình và phần mềm.
2. Gửi metadata các nguồn, crosswalk và extract; thống nhất đường dẫn thật trong manifest.
3. Nối code vào pipeline, kiểm tra mẫu/merge/đơn vị rồi mới kiểm tra hệ số và bảng/hình.
4. Một người khác chạy sạch, đối chiếu benchmark và ghi lại vấn đề còn thiếu.

Không cần công khai microdata để công khai code. Tuy nhiên người tái lập phải có đường tiếp cận hợp pháp và đủ hướng dẫn tạo đúng đầu vào. Nếu một nguồn không thể tiếp cận, ghi rõ giới hạn tái lập đó.
