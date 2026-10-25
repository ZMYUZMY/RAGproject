# RAG 智能客服项目

这是一个基于检索增强生成（RAG）的中文问答示例。项目使用 Chroma 保存向量数据，通过 DashScope 的文本嵌入和聊天模型回答问题，并用本地 JSON 文件保存会话历史。

## 功能

- 上传 TXT 文档并写入本地向量知识库。
- 根据知识库检索相关内容并生成回答。
- 通过 Streamlit 提供知识库上传页和智能客服聊天页。
- 将向量库与会话历史保存在本地目录。

## 项目文件

- `app_qa.py`：智能客服聊天页面。
- `app_file_uploader.py`：TXT 知识库上传页面。
- `rag.py`：RAG 问答链与聊天模型配置。
- `knowledge_base.py`：文本切分、去重和向量入库逻辑。
- `vector_stores.py`：Chroma 向量库与检索器。
- `file_history_store.py`：本地会话历史存储。
- `config_data.py`：向量库路径、分块参数和模型名称。
- `data/`：示例知识库文本。

## 配置与运行

1. 使用 Python 3 创建并激活虚拟环境。
2. 安装项目依赖：Streamlit、LangChain Core、LangChain Community、LangChain Chroma、LangChain Text Splitters 和 DashScope。
3. 设置环境变量 `DASHSCOPE_API_KEY`。例如在 PowerShell 中：

   ```powershell
   $env:DASHSCOPE_API_KEY = "你的 DashScope API Key"
   ```

   该设置仅对当前 PowerShell 窗口有效。请勿把真实密钥写入代码或提交到 Git。
4. 在项目根目录启动所需页面：

   ```powershell
   streamlit run app_qa.py
   ```

   上传知识库页面可通过 `streamlit run app_file_uploader.py` 启动。

首次运行时，Chroma 会在 `chroma_db/` 创建本地向量数据。会话历史保存在 `chat_history/`。这两个目录及虚拟环境、IDE 配置都由 `.gitignore` 排除。
