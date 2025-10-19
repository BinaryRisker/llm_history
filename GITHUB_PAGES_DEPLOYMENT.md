# GitHub Pages 部署指南

## 📚 概述

本指南将帮助你将 `output` 目录中的 HTML 版本书籍部署到 GitHub Pages。

## 🛠️ 已完成的配置

### 1. 创建的文件

- **`output/index.html`**: 作为网站首页的入口点
- **`output/.nojekyll`**: 禁用 Jekyll 处理，确保所有文件都能正常访问
- **`.github/workflows/deploy-pages.yml`**: GitHub Actions 自动部署工作流

### 2. 目录结构

```
llm_history/
├── output/
│   ├── index.html                    # 主入口文件
│   ├── llm-history-chronicle.html    # 原始HTML文件
│   ├── assets/
│   │   └── images/                   # 图片资源
│   ├── config/
│   │   └── html-style.css            # 样式文件
│   └── .nojekyll                     # GitHub Pages 配置
└── .github/
    └── workflows/
        └── deploy-pages.yml          # 自动部署配置
```

## 🚀 部署步骤

### 方法一：使用 GitHub Actions（推荐）

#### 步骤 1: 在 GitHub 仓库中启用 Pages

1. 打开你的 GitHub 仓库页面
2. 点击 **Settings**（设置）
3. 在左侧菜单中找到 **Pages**
4. 在 **Source** 部分，选择：
   - Source: **GitHub Actions**

#### 步骤 2: 提交并推送代码

```bash
# 检查当前状态
git status

# 添加所有新文件
git add output/index.html
git add output/.nojekyll
git add .github/workflows/deploy-pages.yml

# 提交更改
git commit -m "feat: add GitHub Pages deployment configuration"

# 推送到 main 分支
git push origin main
```

#### 步骤 3: 等待部署完成

1. 推送后，GitHub Actions 会自动开始部署
2. 在仓库页面点击 **Actions** 标签查看部署进度
3. 部署完成后，你会看到一个绿色的勾号 ✅
4. 访问 `https://<你的用户名>.github.io/<仓库名>/` 查看你的书籍

### 方法二：手动设置（备选）

如果你不想使用 GitHub Actions，可以使用 `gh-pages` 分支：

#### 步骤 1: 创建 gh-pages 分支

```bash
# 创建一个孤立的 gh-pages 分支
git checkout --orphan gh-pages

# 删除所有文件（我们只需要 output 目录的内容）
git rm -rf .

# 复制 output 目录的内容到根目录
cp -r output/* .
cp output/.nojekyll .

# 提交
git add .
git commit -m "Deploy to GitHub Pages"

# 推送到远程
git push origin gh-pages

# 切回 main 分支
git checkout main
```

#### 步骤 2: 配置 GitHub Pages

1. 进入仓库的 **Settings** → **Pages**
2. 在 **Source** 下选择：
   - Branch: **gh-pages**
   - Folder: **/ (root)**
3. 点击 **Save**

## 📝 访问你的网站

部署完成后，你的书籍将在以下地址可访问：

```
https://<你的GitHub用户名>.github.io/<仓库名>/
```

例如，如果你的用户名是 `BinaryRisker`，仓库名是 `llm_history`，那么地址是：

```
https://BinaryRisker.github.io/llm_history/
```

## 🔧 自动部署说明

使用 GitHub Actions（方法一）的优势：

- ✅ **自动化**: 每次推送到 `main` 分支时自动部署
- ✅ **简单**: 无需手动管理 `gh-pages` 分支
- ✅ **可靠**: GitHub 官方推荐的部署方式
- ✅ **手动触发**: 也可以在 Actions 页面手动触发部署

工作流触发条件：
- 推送到 `main` 分支
- 手动触发（在 Actions 页面点击 "Run workflow"）

## 📋 验证部署

部署完成后，检查以下内容：

1. ✅ 主页能正常加载
2. ✅ 图片资源能正常显示
3. ✅ CSS 样式正确应用
4. ✅ 页面导航功能正常

## ⚠️ 常见问题

### 问题 1: 404 错误

**原因**: GitHub Pages 设置不正确

**解决**:
- 确认 Settings → Pages 中的 Source 设置正确
- 等待 1-2 分钟让 GitHub 完成部署

### 问题 2: 样式丢失

**原因**: 资源路径问题

**解决**:
- 检查 `output/.nojekyll` 文件是否存在
- 确认所有资源文件都在 `output` 目录中

### 问题 3: Actions 部署失败

**原因**: 权限问题

**解决**:
1. 进入 Settings → Actions → General
2. 在 "Workflow permissions" 中选择 "Read and write permissions"
3. 勾选 "Allow GitHub Actions to create and approve pull requests"
4. 点击 Save

## 🔄 更新内容

当你更新书籍内容后，重新生成 HTML 并部署：

```bash
# 假设你已经重新生成了 output 目录中的文件

# 更新 index.html
cp output/llm-history-chronicle.html output/index.html

# 提交并推送
git add output/
git commit -m "update: refresh book content"
git push origin main

# GitHub Actions 会自动部署更新
```

## 📚 其他资源

- [GitHub Pages 官方文档](https://docs.github.com/pages)
- [GitHub Actions 文档](https://docs.github.com/actions)
- [自定义域名设置](https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site)

## ✨ 完成

现在你的 LLM History Chronicle 书籍已经可以通过 GitHub Pages 在线访问了！
