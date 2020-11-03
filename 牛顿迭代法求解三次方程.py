
import sympy as sy
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = "simhei" 
plt.rcParams["axes.unicode_minus"] = False
x=sy.symbols('x')
y = x**3-5*x**2+7*x-3
dy = sy.diff(y,x,1).expand()
x = 10#float(input("请输入迭代初始值："))
ymax = x
n = 100
f = []
x0 = [x]
e = 0.001
xmax = 0
for i in range(n):
    y0 = eval(str(y))
    f.append(y0)
    if sy.Abs(y0-0)<e:
        print('方程的一个解为x1 =',x)
        break
    else:
        x = x - eval(str(y))/eval(str(dy))
        x0.append(x)
        xmax = xmax + 1
plt.xlabel('迭代次数n',fontsize=14)
plt.ylabel('函数值f',fontsize=14)
plt.grid(color='k', linestyle='-.', linewidth=1,alpha=0.5)
fig = plt.figure(figsize=(12,6),dpi = 300)
ax1 = fig.add_subplot(1,1,1)
ax1.grid(color='k', linestyle='-.', linewidth=1,alpha=0.5)
ax1.plot(f,color = 'b',linewidth=2,label='函数值f变化曲线')
ax2 = ax1.twinx()
ax2.plot(x0,color = 'g',linewidth=2,label='迭代变量x变化曲线')
ax1.set_title("牛顿迭代法",size=22) 
ax1.set_xlabel('迭代次数n',size=17)  
ax1.set_ylabel('函数值f',size=17)
ax2.set_ylabel('迭代变量x',size=17)
fig.legend(bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
plt.text(xmax/3,3*ymax/4,'方程的解为x = '+str(x), fontsize=20, color='r')
plt.ylim([0,ymax])
plt.rcParams.update({'font.size': 14})
plt.savefig(r"C:\Users\12139\Desktop\Python_figure\牛顿迭代法.png",dpi=300)
plt.show()
