import numpy as np

# 参数列表,开头全部加一个零，是为了索引与单元标号一致
E = [0, 20000000, 20000000, 40000000, 60000000, 80000000]
Area = [0, 0.0002, 0.0001, 0.0005, 0.0003, 0.0006]
start_point = [-1, 0, 0.1, 0.2, 0.3, 0.4]
end_point = [0, 0.1, 0.2, 0.3, 0.4, 0.5]

# 定义杆单元，用于存储一些杆件的参数
class rod():
    def __init__(self, E, Area, start_point, end_point, i, j):
        self.E = E
        self.Area = Area
        self.start_point = start_point
        self.end_point = end_point
        self.i = i
        self.j = j
        self.length = abs(start_point - end_point)
        # 定义单元的刚度矩阵
        self.k = (Area*E/self.length) * np.array([[1, -1], [-1, 1]])
        # 定义单元的应变矩阵
        self.B = np.array([-1 / self.length, 1 / self.length])
        # 定义应力单元矩阵
        self.S = np.array([-1*E / self.length, E / self.length])

if __name__ == '__main__':
    # 初始化
    num_nodes = 5
    P = 10.000
    rod_system = []
    for n in range(num_nodes+1):
        rod_system.append(rod(E[n], Area[n], start_point[n], end_point[n], n, n+1))

    # print(rod_system[2].E)
    # 创建边界位移条件条件的列表
    U = []
    U.append(0) # 缺省第一项，使索引与单元标号一致
    U.append(0) # U1为零
    for i in range(num_nodes+2):
        U.append('u_unknown')

    # 求解位移函数
    for i in range (num_nodes):
        U[i+2] = P / rod_system[i+1].k[1][1] + U[i+1]
    
    # 计算每个单元的应变
    strain = []
    strain.append(0)
    for i in range(num_nodes):
        strain.append(np.dot(rod_system[i+1].B, np.array([[U[i+1]], 
                                                          [U[i+2]]])))

    # 计算每个单元的应力
    stress = []
    stress.append(0)
    for i in range(num_nodes):
        stress.append(np.dot(rod_system[i+1].S, np.array([[U[i+1]], 
                                                          [U[i+2]]])))
    for i in range(num_nodes+1):
        print("第{}个节点，该节点的位移为{:.6f}".format(i+1, U[i+1]))
    for i in range(num_nodes):
        print("第{}个单元，该单元的应变为{:.6f}，应力为{:.6f}".format(i+1, strain[i+1].item(), stress[i+1].item()))
    
    # 计算任意一点的位移
    x = input("请输入坐标x=")
    x = float(x)
    # x = 0.15
    for i in range(num_nodes):
        if (x >= rod_system[i+1].start_point) and (x <= rod_system[i+1].end_point):
            x = x - rod_system[i+1].start_point
            N = np.array([1-x/rod_system[i+1].length, x/rod_system[i+1].length])
            delta_x = np.dot(N, np.array([[U[i+1]], 
                                          [U[i+2]]])).item()
            print("该点位于第{}根杆上".format(i+1))
            print("该坐标的位移为{:.6f}".format(delta_x))
            print("该点的应变为{:.4f}".format(strain[i+1].item()))
            print("该点的应力为{:.4f}".format(stress[i+1].item()))
        else:
            continue
    # print(np.dot(rod_system[0+1].B, np.array([[U[0+1]], 
    #                                           [U[0+2]]])).item())
    # print(strain[1])
    # for i in range(num_nodes+2):
    #     print((i, U[i]), end="\n")

    # print(P / rod_system[1].k[1][1])
