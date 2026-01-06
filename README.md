# 基于 Gemini API 的医学化验单批量识别与结构化流程

## Abstract
本流程旨在解决传统 OCR 工具对复杂排版医学化验单（Medical Lab Reports）识别率低、缺乏语义理解的问题。通过 Python 脚本批量调用多模态大模型（Gemini 1.5 Flash），实现从图片到标准 CSV 表格的自动化转换。

## Context
* **Problem:** 临床科研中存在大量纸质或图片格式的化验单，手动录入效率低且易出错；传统 OCR（如 Tesseract）难以处理歪斜、污渍及复杂的表格线，且无法自动纠正语义错误（如单位识别）。
* **Solution:** 利用 Gemini 1.5 Flash 的长上下文和视觉理解能力，直接读取图片并提取 key-value 数据，输出为标准化的 CSV 格式，便于直接导入 R 或 Python 进行下游分析。
