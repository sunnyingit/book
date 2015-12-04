# sublime 配置

------
### 1 使用心得
-  使用```command+shift+p```快速查找命令，用户配置，插件设置等任何你能想到的关于sublime的信息，不要再使用鼠标去点击了

-  使用vim模式，配合sublime，感受疾如风，不要再使用鼠标了

-  sublime 自动提示php代码，实时保存，文件，函数快速定位，不要再使用鼠标了

-  漂亮的不像实力派

-  安装插件，主题，修改默认键，用户配置，勤点击sublime提供的功能

-  按下ESC 去掉自动提示


### 2 这是我的sublime
![file-list](http://hellosunli-wordpress.stor.sinaapp.com/blog-uploads/998074.png)

### 3 安装插件
1 使用ctrl+` 调出命令行
2 输入 ```
import urllib.request,os,hashlib; h = '7183a2d3e96f11eeadd761d777e62404' + 'e330c659d4bb41d3bdf022e94cab3cd0'; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); by = urllib.request.urlopen( 'http://sublime.wbond.net/' + pf.replace(' ', '%20')).read(); dh = hashlib.sha256(by).hexdigest(); print('Error validating download (got %s instead of %s), please try manual install' % (dh, h)) if dh != h else open(os.path.join( ipp, pf), 'wb' ).write(by) ```

3 关掉 ``` command +q  ``` 再打开

4 使用 ``` command + shift + p ``` 调出命令板，输入install packages



### 4 用户配置

```python
{
    "always_show_minimap_viewport": false,
    "auto_match_enabled": true,
    "bold_folder_labels": true,
    // 需要安装material 主题插件
    "color_scheme": "Packages/User/Material-Theme (Flake8Lint).tmTheme",
    "draw_white_space": "all",
    "ensure_newline_at_eof_on_save": true,
    "font_size": 14,
    "highlight_line": true,
    "highlight_modified_tabs": true,
    // sublime 默认ignore了vim模式，按ESC进入vim模式
    "ignored_packages":[],
    "line_padding_bottom": 3,
    "line_padding_top": 3,
    "material_theme_accent_lime": true,
    "material_theme_bold_tab": true,
    "material_theme_disable_fileicons": true,
    "material_theme_panel_separator": true,
    "material_theme_small_tab": true,
    "material_theme_tabs_autowidth": true,
    "overlay_scroll_bars": "enabled",
    "remember_full_screen": true,
    // 让你的python代码不要写的太长了
    "rulers":
    [
        80, 100
    ],
    // 需要安装sublimelinter插件
    "sublimelinter_popup_errors_on_save": true,
    "theme": "Material-Theme.sublime-theme",
    // 之前我没有打开这个选项，导致代码上传到github 显示全乱
    "translate_tabs_to_spaces": true,
    // 保存时，去掉多余的空格
    "trim_trailing_white_space_on_save": true
    // 保存时，在文件末尾增加一空行，规范
    "ensure_newline_at_eof_on_save": false,
}

```

### 5 定制快捷键

```python
    // 对齐
    { "keys": ["ctrl+y"], "command": "alignment" },
    // 多次按ctrl+d，可以选中多个然后多次编辑,像vim块操作一样6
    { "keys": ["ctrl+d"], "command": "duplicate_line" },
    // 查找
    { "keys": ["ctrl+k"], "command": "slurp_find_string" },
    // 删除一行
    { "keys": ["ctrl+e"], "command": "run_macro_file", "args": {"file": "Packages/Default/Delete Line.sublime-macro"} },
    // 复制的时候，自动缩进
    { "keys": ["super+v"], "command": "paste_and_indent" },
    // 使用super+d选择区域，按下super+l，这个时候如果直接输入，则会删除原来选择的数据，相当于replace效果
    // 如果想再选中一块区域前面插入数据，则需要移动方向键，这也光标就会变成插入状态，试一试你就知道，
    { "keys": ["super+l"], "command": "split_selection_into_lines" },
    // 选中一块区域， 按下快捷键，把多行变成一行
    { "keys": ["super+j"], "command": "join_lines" },
    //  全屏
    { "keys": ["super+m"], "command": "toggle_full_screen" },
    // 替换
    { "keys": ["super+h"], "command": "show_panel", "args": {"panel": "replace", "reverse": false} },
    // 把行移動到上面
    { "keys": ["super+up"], "command": "swap_line_up" },
    // 移動行到下面
    { "keys": ["super+down"], "command": "swap_line_down" },
    // 關閉右邊的文件夾
    { "keys": ["super+b"], "command": "toggle_side_bar" },
    // 打開命令行
    { "keys": ["super+shift+p"], "command": "show_overlay", "args": {"overlay": "command_palette"}},
    // 大写
    { "keys": ["super+u"], "command": "upper_case" },
    // 小写
    { "keys": ["super+l"], "command": "lower_case" },
    // 选中函数跳转到调用的地方
    { "keys": ["super+g"], "command": "goto_definition" }

```

### 6 Web开发插件
学习插件最好的方法就是自己动手，使用 command+shift+p 查看插件的配置，快捷键

```
Bracket Highlighter:  语法高亮

alignment: 使选中一块区域按照“=”对齐，可以快速美化代码

git: 可以使用git任意命令，我常使用的git blame 查看文件被谁修改，找人背锅利器

gitgutter: 编辑git仓库里面的文件，会显示文件的“修改，删除，添加”状态

ctags:  使用ctags之前，必须先安装ctags, Mac 系统 使用 brew install ctags, 安装之后，选中一个目录，ctrl+r 生成一个tags记录，使用ctrl+t查找文件，ctags只能提示函数在那里定义，不能提示在哪里调用 文档：https://github.com/SublimeText/CTags

build .tags文件的时候，可能会提示一个错误 'illege option -R',是因为Mac自带的ctags命令不支持—R命令,修复思路就是使用brew 安装的ctags命令覆盖原来的ctags命令， alias ctags='`brew --prefix`/bin/ctags'


Cscope: 详细文档在：https://github.com/ameyp/CscopeSublime

thriftSyntax: thrfit文件语法高亮

DocBlockr: 输入/** 然后按下tab键，你会有所发现

atuopep8: python格式化插件

jedi: 安装好之后，可以自动补全python代码

Python flake8 int: python 语法提示

PHPcs: php语法，风格检测等，文档：https://github.com/benmatselby/sublime-phpcs

jsformat: js格式化

sublimeREPl: 可以在sublime里面开一个python终端

subllimeLinter: 语法检测插件

vim Navigatino: vim插件

Material Theme: 主题插件，必装

```

当你某个功能使用的不爽的时候，就去查找插件把，终有一款属于你

## 最快的使用方式

使用的时候，可以想怎么才能更快使用sublime,分屏操作，最大化，隐藏各种status bar

怎么最快的文件，创建新文件，搜索，替换，各种移动，各种删除，快操作，sublime可以的和vim一样，不需要鼠标就可以操作

达到这种境界，只有多看sublime的tools，files, views, edit提供的操作键

```python
command+q 退出
command+r 查找文件里面的所有的函数
command+p 输入所在目录,或者文件名，sublime会模糊匹配
command+n 创建新文件
commadn+w 关闭一个tab
command+alt+2 分成两屏
```





