# data 目录（负责人：组员 C）

## 目录约定

- `raw/`：原始文档（PDF / Word），放 10～20 份
- `ingest.py`：解析与切块脚本（待组员 C 编写）
- `chunks.json`：切块结果，**后端直接读取这个文件**
- `test_questions.json`：测试问题集（待组员 C 编写）

目前的 `chunks.json` 只有 3 条示例数据，供大家开发联调用，组员 C 完成后整体替换。

## chunks.json 格式（不得更改字段名）

```json
[
  {
    "chunk_id": "文档简称_p页码_c序号",
    "doc_name": "原始文件名.pdf",
    "page": 3,
    "content": "文本块内容"
  }
]
```

## test_questions.json 格式

```json
[
  {
    "question": "三天以上的请假由谁审批？",
    "answer": "需经人力资源部复核",
    "source_chunk_ids": ["sample_p1_c2"]
  }
]
```

`source_chunk_ids` 填写答案所在的文本块，下一阶段用来计算检索命中率。

## 建议

- PDF 解析：`pypdf` 或 `pdfplumber`；Word 解析：`python-docx`
- 切块：每块 300～500 字，相邻块重叠 50～100 字，尽量按段落切，不要把一句话切断
- 文档挑内容扎实、能出题的，如学校规章制度、课程讲义、公开的产品手册
