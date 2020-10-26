import numpy as np
type_concrete = input("请输入混凝土强度等级(如C30):")
type_stress = input("请输入钢筋种类(如HPB300):")
degere = input("请输入安全等级(如一级):")
r0 = {'一级': 1.1, '二级': 1.0, '三级':0.9}[degere]
index_x = [x for x,y in zip(list(range(1,4)),['300','400','500']) if y == type_stress[-3:]]
index_y = [x for x,y in zip(list(range(1,6)),list(range(50,75,5))) if y == int(type_concrete[-2:])]
if index_y == []:
   index_y = [0]
g_b = ([0.58,0.56,0.56,0.54,0.54],[0.53,0.51,0.51,0.49,0.49],[0.49,0.47,0.47,0.46,0.46])[index_x[0]-1][index_y[0]-1]
f_sd = [250,330,415][index_x[0]-1]     
f_cd = [11.5,13.8,16.1,18.4,20.5,22.4,24.4,26.5,28.5,30.5,32.4,34.6][int((int(type_concrete[-2:])-25)/5)]
f_td = [1.23,1.39,1.52,1.65,1.74,1.83,1.89,1.96,2.02,2.07,2.10,2.14][int((int(type_concrete[-2:])-25)/5)]
print("\n\033[1;31;47m\t重要性系数r0: %0.1f \033[0m"%r0)
print("\033[1;31;47m\t相对界限受压区高度g_b: %0.2f \033[0m"%g_b)
print("\033[1;31;47m\t混凝土轴心抗压强度f_cd: %0.2f MPa\033[0m"%f_cd)
print("\033[1;31;47m\t钢筋抗拉强度设计值f_sd: %0.2f MPa\033[0m"%f_sd)
b = float(input("请输入截面尺寸b(mm):"))
h = float(input("请输入截面尺寸h(mm):"))
M_d = float(input("请输入截面弯矩设计值Md(KN*m):"))
#分别计算铺设单层钢筋，双层钢筋下的各个参数以及最小配筋率
a_s1 = 40
a_s2 = 70
h01 = h-a_s1
h02 = h-a_s2
x1 = np.round(h01-np.sqrt(h01*h01-(2*r0*M_d)/(f_cd*b)*1000000),0)
x2 = np.round(h02-np.sqrt(h02*h02-(2*r0*M_d)/(f_cd*b)*1000000),0)
g = x1/h01
As01 = f_cd*b*x1/f_sd
As02 = f_cd*b*x2/f_sd
As0 = min(As01,As02)
p_min = max(45*f_td/f_sd,0.2)
#打印参数
print("\n\033[1;31;47m\t截面受压区高度为x0(按单层设计): %0.0f mm\033[0m"%x1)
print("\033[1;31;47m\t截面受压区高度为x0(按双层设计): %0.0f mm\033[0m"%x2)
print("\033[1;31;47m\t所需钢筋面积为As(按单层设计): %0.0f mm^2\033[0m"%As01)
print("\033[1;31;47m\t所需钢筋面积为As(按双层设计): %0.0f mm^2\033[0m"%As02)
print("\033[1;31;47m\t最小配筋率为: %0.2f %%\033[0m"%p_min)
print("\n\033[1;30;47m\t单筋矩形截面设计方案如下:\033[0m")
#钢筋面积，直径表
list_As = ([28.3,57,85,113,141,170,198,226,254],[50.3,101,151,201,251,302,352,402,452],
               [78.5,157,236,314,393,471,550,628,707],[113.1,226,339, 452,566,679,792,905,1018],
               [153.9,308,462,616,770,924,1078,1232,1385],[201.1,402,603,804,1005,1206,1407,1608,1810],
               [254.5,509,763,1018,1272,1527,1781,2036,2290],[314.2,628,942,1256,1570,1884,2200,2513,2827],
               [380.1,760,1140,1520,1900,2281,2661,3041,3421],[490.9,982,1473,1964,2454,2945,3436,3927,4418],
               [615.8,1232,1847,2463,3079,3695,4310,4926,5542],[804.2,1608,2413,3217,4021,4826,5630,6434,7238])
list_d0 = [7.0,9.3,11.6,13.9,16.2,18.4,20.5,22.7,25.1,28.4,31.6,35.8]
list_d = list(range(6,24,2))+([25,28,32])
#找到合适的钢筋
d = []
d0 = []
n = []
As = []
As_min = 0.05
As_max = 0.35
for index1, val1 in enumerate(list_As):
    for index2, val2 in enumerate(val1):
        if (1-As_min)*As0<val2<(1+As_max)*As0:
            d0.append(list_d0[index1])
            d.append(list_d[index1])
            n.append(index2+1)
            As.append(val2)         
#矩阵转置函数
def transpose(x,y):
    matric = [x,y]
    trans = [[matric[j][i] for j in range(len(matric))] for i in range(len(matric[0]))]
    return trans
#拼接每一组合[n,d0,d,As]
trans_d = transpose(d,d)
trans_As = transpose(As,As)
trans_nd0 = transpose(n,d0)
temp0 = np.delete(np.hstack((trans_nd0,trans_d)),2,1)
temp = np.delete(np.hstack((temp0,trans_As)),4,1)

#满足要求的单层钢筋
A_single_layer = [[i,j,k,l] for i,j,k,l in temp if 1<i<5 and ((20+10+j/2)*2+(i-1)*j+(i-1)*30<b)]
#满足要求的双层钢筋
Double_layer = [[i,j,k,l] for i,j,k,l in temp if i>4 and ((i%2==0 and ((20+10+j/2)*2+(i/2-1)*j+(i/2-1)*30<b)) 
       or (i%2==1 and ((20+10+j/2)*2+((i+1)/2-1)*j+((i+1)/2-1)*30<b)))]
#打印配筋方案
k = 1
for i in range(np.shape(A_single_layer)[0]):
    print("\n\033[1;30;43m\t设计方案%0.0f：\033[0m"%k)
    print("\033[1;35;47m\t铺设单层钢筋：\033[0m")
    print("\033[1;34;47m\t钢筋公称直径d: %0.0fmm\033[0m"%A_single_layer[i][2])
    print("\033[1;34;47m\t钢筋根数为: %0.0f根\033[0m"%A_single_layer[i][0])
    print("\033[1;34;47m\t钢筋面积为: %0.0fmm^2\033[0m"%A_single_layer[i][3])
    print("\033[1;34;47m\t布置净距Sn: %0.0fmm\033[0m"%((b-2*a_s1-(A_single_layer[i][0]-1)*A_single_layer[i][1])/((A_single_layer[i][0]-1))))
    print("\033[1;34;47m\t配筋率为: %0.2f%%\033[0m"%(A_single_layer[i][3]/(b*h01)*100))
    k += 1
for i in range(np.shape(Double_layer)[0]):
    print("\n\033[1;30;43m\t设计方案%0.0f：\033[0m"%k)
    print("\033[1;35;47m\t铺设双层钢筋：\033[0m")
    print("\033[1;34;47m\t钢筋公称直径d: %0.0fmm\033[0m"%Double_layer[i][2])
    print("\033[1;34;47m\t钢筋根数为: %0.0f根\033[0m"%Double_layer[i][0])
    print("\033[1;34;47m\t钢筋面积为: %0.0fmm^2\033[0m"%Double_layer[i][3])
    print("\033[1;34;47m\t布置净距Sn: %0.0fmm\033[0m"%((b-2*40-(np.floor((Double_layer[i][0]+1)/2)-1)*Double_layer[i][1])/(np.floor((Double_layer[i][0]+1))/2-1)))
    print("\033[1;34;47m\t配筋率为: %0.2f%%\033[0m"%(Double_layer[i][3]/(b*h02)*100))
    k += 1
