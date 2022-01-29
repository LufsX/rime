# [Rime](https://blog.isteed.cc/post/rime-2022/)

[我的 Rime 配置文件～](https://blog.isteed.cc/post/rime-2022/)

## macOS

- OS: macOS 10.15.7
- Version: [0.15.2-a9829e8](https://storage.isteed.cc/MacSoftware/Squirrel)
- Date: 2022-01-27

### 下载

最新的鼠须管，[点击下载](https://cdn.isteed.cc/file/squirrel/Squirrel-0.15.2-a9829e8.pkg)即可

自己编译的，就合了两 PR，具体源码可以看 [LufsX/squirrel](https://github.com/LufsX/squirrel)

## Windows

> 个人主要使用 macOS，所以这个配置可能会有些小问题～

- OS: Windows 10 20H2
- Version: [0.14.3.0](https://gh.isteed.cc/https://github.com/rime/weasel/releases/download/0.14.3/weasel-0.14.3.0-installer.exe)
- Date: 2022-01-27

# 预览

![p1](https://cdn.isteed.cc/img/rime-2022/p1.png)![p2](https://cdn.isteed.cc/img/rime-2022/p2.png)![p3](https://cdn.isteed.cc/img/rime-2022/p3.png)![p4](https://cdn.isteed.cc/img/rime-2022/p4.png)![p5](https://cdn.isteed.cc/img/rime-2022/p5.png)

![f1](https://cdn.isteed.cc/img/rime-2022/f1.png)![f2](https://cdn.isteed.cc/img/rime-2022/f2.png)![f3](https://cdn.isteed.cc/img/rime-2022/f3.png)![f4](https://cdn.isteed.cc/img/rime-2022/f4.png)

# 安装

macOS 安装步骤：

1. 备份原有配置（如果有的话）
2. 打开 `用户设定`
3. 将本仓库所有文件复制到 `用户设定` 文件夹中
4. 重新部署鼠须管

Windows 安装步骤：

1. 备份原有配置
2. 打开 `用户文件夹`
3. 将本仓库所有文件复制到 `用户文件夹` 中
4. 取消 `lufs_flypy.schema.yaml` 与 `lufs_pinyin.schema.yaml` 文件中 30 行左右的注释
5. 重新部署小狼毫

## 小技巧

- 国内 GitHub 下载缓慢/无法下载可以尝试使用 [Cloudflare 加速下载](https://gh.isteed.cc/https://github.com/LufsX/rime/archive/refs/heads/master.zip)
- 或使用 [Gitee 镜像](https://gitee.com/LufsX/rime)（须登录，不推荐使用）

# 特性

- 「小鹤双拼」+「朙月拼音」
- 模糊音
- Emoji 支持
- 8104 简体字
- 朙月拼音支持按键纠错与容错拼写
- `Caps` 切换英文输入法
- 长句模型
- THUOCL 词库
- 搜狗词库（夹带私货）
- 自定义词典（自造词）
- 词库总大小仅 `7.2MB`（包括八股文仅 `10MB`）
- 快捷输入（日期，时间，星期）
- 以词定字

# 使用

详见 [我的 Rime 配置文件～](https://blog.isteed.cc/post/rime-2022/)

# 待办

- [x] 更新搜狗词库 Update: 2022-01-04
- [x] 添加深色主题
- [x] 添加 Emoji 支持
- [ ] ~~添加「[同文输入法](https://github.com/osfans/trime)」支持~~（Android 12 似乎不兼容，无法测试）
- [x] 添加模糊拼音支持
- [ ] 更好的词库与词频？
- [x] 更加适配小狼毫的配置

# 感谢/参考

- [BlindingDark/rime-lua-select-character](https://github.com/BlindingDark/rime-lua-select-character)
- [KyleBing/rime-wubi86-jidian](https://github.com/KyleBing/rime-wubi86-jidian/)
- [lotem/luna_pinyin.custom.yaml](https://gist.github.com/lotem/2320943)
- [maomiui/rime](https://github.com/maomiui/rime)
- [placeless/squirrel_config](https://github.com/placeless/squirrel_config)
- [rime/squirrel](https://github.com/rime/squirrel)
- [thunlp/THUOCL](https://github.com/thunlp/THUOCL)
- [搜狗词库](https://pinyin.sogou.com/dict/)
