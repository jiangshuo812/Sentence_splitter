# 英语文本句子分割器

这是一个使用spaCy实现的英语文本句子分割工具，可以将英语文段准确地分割成单独的句子。

## 功能特点

- 支持txt和docx格式的输入文件
- 使用spaCy进行准确的句子分割
- 自动处理常见缩写（如Dr.、U.S.A.等）
- 输出格式化的JSON结果
- 完整的错误处理和日志记录

## 安装要求

1. Python 3.7+
2. 必要的Python包（见requirements.txt）

## 安装步骤

1. 克隆或下载本项目
2. 安装依赖：
```bash
pip install -r requirements.txt
```
3. 下载spaCy的英语语言模型：
```bash
python -m spacy download en_core_web_sm
```

## 使用方法

1. 准备输入文件（.txt或.docx格式）
2. 运行脚本：
```bash
python sentence_splitter.py
```
3. 查看输出结果（默认保存为output.json）

## 输出格式

输出文件为JSON格式，包含以下内容：
```json
{
  "total_sentences": 数量,
  "sentences": [
    "句子1",
    "句子2",
    ...
  ]
}
```

## 日志

- 程序运行日志保存在`sentence_splitter.log`文件中
- 日志包含详细的运行信息和错误记录

## 注意事项

- 确保输入文件使用UTF-8编码
- 对于大文件处理，建议确保有足够的系统内存
- 首次运行时会自动下载spaCy语言模型 