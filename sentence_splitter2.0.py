import os 

current_path = os.path.dirname(os.path.abspath(__file__))

os.chdir(current_path)

import spacy
import json
from pathlib import Path
from typing import List, Dict
from loguru import logger
import docx
from spacy.language import Language
import re

class SentenceSplitter:
    def __init__(self):
        """初始化SentenceSplitter类"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("成功加载spaCy模型")
        except OSError:
            logger.error("spaCy模型未找到，正在下载...")
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy模型下载完成")

    def read_text_file(self, file_path: str) -> str:
        """读取文本文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"读取文件时出错: {str(e)}")
            raise

    def read_docx_file(self, file_path: str) -> str:
        """读取Word文档内容"""
        try:
            doc = docx.Document(file_path)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            logger.error(f"读取Word文档时出错: {str(e)}")
            raise

    def is_complete_sentence(self, sentence: str) -> bool:
        """判断是否为完整句子"""
        # 定义完整句子的标准：
        # 1. 必须包含主谓结构（通过spaCy的依存分析）
        # 2. 必须以合适的标点符号结尾（.!?）
        # 3. 必须以大写字母开头
        doc = self.nlp(sentence.strip())
        
        # 检查句子是否以大写字母开头
        if not sentence.strip() or not sentence.strip()[0].isupper():
            return False
            
        # 检查句子是否以合适的标点符号结尾
        if not re.search(r'[.!?]$', sentence.strip()):
            return False
            
        # 检查主谓结构
        has_subject = False
        has_verb = False
        
        for token in doc:
            if token.dep_ in ['nsubj', 'nsubjpass']:  # 主语
                has_subject = True
            if token.pos_ == 'VERB':  # 谓语动词
                has_verb = True
                
        return has_subject and has_verb

    def split_sentences(self, text: str) -> List[Dict]:
        """将文本分割成句子，并添加ID"""
        try:
            doc = self.nlp(text)
            sentences = []
            sentence_id = 1
            
            for sent in doc.sents:
                sentence_text = sent.text.strip()
                if self.is_complete_sentence(sentence_text):
                    sentence_obj = {
                        "id": sentence_id,
                        "text": sentence_text
                    }
                    sentences.append(sentence_obj)
                    sentence_id += 1
                else:
                    logger.warning(f"跳过非完整句子: {sentence_text}")
                    
            logger.info(f"成功分割出 {len(sentences)} 个完整句子")
            return sentences
        except Exception as e:
            logger.error(f"分割句子时出错: {str(e)}")
            raise

    def process_file(self, input_path: str, output_path: str) -> None:
        """处理输入文件并保存结果"""
        try:
            # 确定文件类型并读取内容
            input_path = Path(input_path)
            if input_path.suffix.lower() == '.docx':
                text = self.read_docx_file(str(input_path))
            else:
                text = self.read_text_file(str(input_path))

            # 分割句子
            sentences = self.split_sentences(text)

            # 构建输出数据
            output_data = {
                "total_sentences": len(sentences),
                "sentences": sentences
            }

            # 保存结果为txt文件
            with open(output_path, 'w', encoding='utf-8') as f:
                for sentence in sentences:
                    f.write(f"ID: {sentence['id']}\n")
                    f.write(f"Text: {sentence['text']}\n")
                    f.write("-" * 80 + "\n")  # 分隔线
            
            logger.info(f"结果已保存到 {output_path}")

        except Exception as e:
            logger.error(f"处理文件时出错: {str(e)}")
            raise

def main():
    # 配置日志
    logger.add("sentence_splitter.log", rotation="500 MB")
    
    try:
        splitter = SentenceSplitter()
        
        # 示例用法
        input_file = "test_1.txt"  # 或 "input.docx"
        output_file = "sentences_v2.txt"
        
        splitter.process_file(input_file, output_file)
        
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        raise

if __name__ == "__main__":
    main() 