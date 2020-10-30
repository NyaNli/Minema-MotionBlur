# Minema 运动模糊编码插件

原理挺简单的，就提高录制帧率，然后每固定数量的帧求平均值合并成一帧，以此模拟现实中长曝光实现的运动模糊效果  
实际上直接在minema里写这个功能用OpenGL作合成效率最高，不过我没有Forge的编译环境，就只好写了个第三方程序放在MOD与FFMpeg中间做图像处理  

### 为什么不用光影的动态模糊
那玩意只有在镜头动的时候才会做个径向模糊，根本不是啥动啥模糊的运动模糊

### 下载地址：
页面右侧的Release可以下载打包好的exe文件  

### 安装方法：  
![安装位置](https://user-images.githubusercontent.com/20377926/97544518-b0015200-1a04-11eb-9f21-56b82f5d4ae9.png)  
将MotionBlur.exe和ffmpeg.exe放在一起  
MotionBlur.exe只起到运动模糊的合成过程，实际视频输出还是要用ffmpeg的  
![编码参数](https://user-images.githubusercontent.com/20377926/97544523-b1cb1580-1a04-11eb-8ab2-f0fb49e126d4.png)  
MotionBlur额外在这里增加了一个可选的mb_frames参数，用来确定将多少帧合并为一帧，不写这个参数的话默认是10帧，这个参数同时也决定了模糊量  
编码器参数里的ffmpeg参数不用做修改，MotionBlur会自动处理并传递给ffmpeg  
![帧率参数](https://user-images.githubusercontent.com/20377926/97544526-b394d900-1a04-11eb-9eab-6c4a4a163925.png)  
minema的捕获帧率=输出视频的帧率*mb_frames参数  
比如这里要输出24fps的视频，mb_frames参数为10，minema里就填240  
至少要填个能被mb_frames整除的数不然说不定会出什么bug  
之后正常录制就OK了，录制出来就是带运动模糊的  
注：设置界面的帧率有240的上限，游戏中Shift+F4弹出界面里的帧率没有上限  
注2：超高帧率会导致BlockBuster在一些速度较快的动画中出现补间不连贯的情况，建议做运动速度超级快的分镜的时候整体放慢，渲染时再用minema的引擎速率功能加速获得正常速度的动画  

我自己目前用着没啥Bug，咱现实很忙的不负责解答疑问  
如果出了问题，一个可选的替代方案是关闭Minema的编码直接输出高帧率的序列帧，然后导入视频编辑软件用帧混合模式降低帧率，效果理论上是一样的
