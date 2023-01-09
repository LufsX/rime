# [Rime](https://blog.isteed.cc/post/rime-2022/)

[我的 Rime 配置文件～](https://blog.isteed.cc/post/rime-2022/)

- [macOS 安装说明](##macOS)
- [Windows 安装说明](##Windows)
- [Android 安装说明](##Android)

# 预览

![p1](https://cdn.isteed.cc/img/rime-2022/p1.png)![p2](https://cdn.isteed.cc/img/rime-2022/p2.png)![p3](https://cdn.isteed.cc/img/rime-2022/p3.png)![p4](https://cdn.isteed.cc/img/rime-2022/p4.png)![p5](https://cdn.isteed.cc/img/rime-2022/p5.png)

![f1](https://cdn.isteed.cc/img/rime-2022/f1.png)![f2](https://cdn.isteed.cc/img/rime-2022/f2.png)![f3](https://cdn.isteed.cc/img/rime-2022/f3.png)![f4](https://cdn.isteed.cc/img/rime-2022/f4.png)

## 小技巧

- 国内 GitHub 下载缓慢/无法下载可以尝试使用 [Cloudflare 加速下载](https://cors.isteed.cc/https://github.com/LufsX/rime/archive/refs/heads/master.zip)

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
- [x] 添加「[同文输入法](https://github.com/osfans/trime)」支持
- [x] 添加模糊拼音支持
- [ ] 更好的词库与词频？
- [ ] 更好的适配「小狼毫」
- [ ] 更好的适配「同文输入法」
- [ ] 脚本自动部署/更新

欢迎提 ISSUE/PR 哈～（虽然我觉得都没人看

## macOS

- OS: macOS Ventura
- Version: [2023-01-09(0.15.2)](https://storage.isteed.cc/MacSoftware/Squirrel/Squirrel-2023-01-09.pkg)
- Date: 2023-01-09

### 下载

最新的鼠须管，[点击下载](https://cdn.isteed.cc/file/squirrel/Squirrel-2023-01-09.pkg)即可

自己编译的，就合了个 PR，具体源码可以看 [LufsX/squirrel](https://github.com/LufsX/squirrel)

### 安装步骤

1. 备份原有配置（如果有的话）
2. 下载[仓库压缩包](https://cors.isteed.cc/https://github.com/LufsX/rime/archive/refs/heads/master.zip)并解压
3. 打开 `用户设定`
4. 将本仓库所有文件复制到 `用户设定` 文件夹中
5. 重新部署鼠须管

## Windows

> 个人主要使用 macOS，所以其它平台的配置可能会有些小问题～

- OS: Windows 10 20H2
- Version: [0.14.3.0](https://cors.isteed.cc/https://github.com/rime/weasel/releases/download/0.14.3/weasel-0.14.3.0-installer.exe)
- Date: 2022-01-27

### 安装步骤

1. 备份原有配置（如果有的话）
2. 下载[仓库压缩包](https://cors.isteed.cc/https://github.com/LufsX/rime/archive/refs/heads/master.zip)并解压
3. 打开 `用户文件夹`
4. 将本仓库所有文件复制到 `用户文件夹` 中
5. 取消 `lufs_flypy.schema.yaml` 与 `lufs_pinyin.schema.yaml` 文件中 30 行左右的注释
6. 重新部署小狼毫

## Android

> 个人主要使用 macOS，所以其它平台的配置可能会有些小问题～

- OS: Android 13
- Version: [652a867](https://github.com/osfans/trime/suites/7541740718/artifacts/311071325)
- Date: 2022-07-27

推荐下载最新的 CI 版 [TRIME](https://github.com/osfans/trime/actions)，登录 GitHub 后点开 `commit ci`，再点开最新的 `run`，拉到最下面，下载 `trime_arm64_v8a` 解压安装即可

### 安装步骤

1. 备份原有配置（如果有的话）
2. 下载[仓库压缩包](https://cors.isteed.cc/https://github.com/LufsX/rime/archive/refs/heads/master.zip)并解压
3. 使用文件管理器打开 `内置存储空间/rime/` 文件夹
4. 将本仓库所有文件复制到 `内置存储空间/rime/` 中
5. 打开 `同文输入法` - `方案` 选择对应方案后确定即可

# 感谢/参考

- [BlindingDark/rime-lua-select-character](https://github.com/BlindingDark/rime-lua-select-character)
- [KyleBing/rime-wubi86-jidian](https://github.com/KyleBing/rime-wubi86-jidian/)
- [lotem/luna_pinyin.custom.yaml](https://gist.github.com/lotem/2320943)
- [maomiui/rime](https://github.com/maomiui/rime)
- [placeless/squirrel_config](https://github.com/placeless/squirrel_config)
- [rime/rime-prelude](https://github.com/rime/rime-prelude)
- [rime/squirrel](https://github.com/rime/squirrel)
- [thunlp/THUOCL](https://github.com/thunlp/THUOCL)
- [搜狗词库](https://pinyin.sogou.com/dict/)
