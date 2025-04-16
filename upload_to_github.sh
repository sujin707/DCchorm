# 配置Git
git config --global user.name "sujin707"
git config --global user.email "1976191081@qq.com"


# 切换到代码所在文件夹
cd D:/afsafafafafafafsfsf/DCProject

# 初始化本地仓库
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "首次提交代码"

# 关联远程仓库
git remote add origin https://github.com/sujin707/DCchorm.git

# 推送代码到GitHub
git push -u origin main
