# Bài tập lớn Xử lý ngôn ngữ tự nhiên
Hệ thống Hỏi & Đáp thông tin các chuyến tàu.

## Cấu trúc thư mục

```
.
├── models/        # Các modules hiện thực
│   ├── global_vars.py       # Các biến toàn cục
│   ├── preprocess.py        # Tiền xử lý dữ liệu
│   ├── maltparse.py         # Phân tích văn phạm phụ thuộc
│   ├── grammar_relation.py  # Chuyển sang quan hệ văn phạm
│   ├── logical_form.py      # Chuyển sang dạng luận lý
│   ├── semantic_procedure.py  # Tạo ngữ nghĩa thủ tục
│   └── execute.py           # Truy xuất dữ liệu
├── input/         # Đầu vào, dữ liệu cho chương trình
│   ├── database.txt         # Chứa dữ liệu các chuyến tàu
│   └── questions.txt        # Chứa các câu hỏi
├── output/        # Đầu ra của chương trình
└── main.py        # Entry point
```

## Chạy chương trình
- Yêu cầu: Python 3.7+

### Truy xuất bằng file
Lệnh dưới sẽ phân tích tất cả các câu hỏi có trong file `input/questions/` và xuất ra ouput cho từng câu vào thư mục `output/`
```
python main.py
```

### Truy xuất trực tiếp trên command line
Dùng option `-s` để nhập trực tiếp câu hỏi trên command line:
```
$ python main.py -s "Tàu hoả B2 có chạy đến Hà Nội không?"
Câu hỏi: Tàu hoả B2 có chạy đến Hà Nội không?
Trả lời: Không.
```

Thêm option `-v` để in ra chi tiết output các bước phân tích:
```
$ python main.py -s "Tàu hoả B2 có chạy đến Hà Nội không?" -v
Câu hỏi: Tàu hoả B2 có chạy đến Hà Nội không?

** Dependencies **
"b2" --nmod-> "tàu_hoả"
"chạy" --subj-> "b2"
"ROOT" --root-> "chạy"
"chạy" --pp-> "đến"
"đến" --pmod-> "hà_nội"
"chạy" --yesno-> "không"
"chạy" --punc-> "?"

** Grammar Relations **
(s1 TRAIN b2)
(s1 PRED chạy)
(s1 DES hà_nội)
(s1 YESNO không)

** Logical Form **
(YESNO  (chạy s1 (TRAIN  b2) (TO-LOC  hà_nội)))

** Procedure **
(EXISTS ?y (TRAIN B2) (ATIME B2 HN ?t))

Trả lời: Không.
```
