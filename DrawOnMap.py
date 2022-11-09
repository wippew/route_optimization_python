from Utils import get_color_by_type, order_correctly
import matplotlib.pyplot as plt
import pulp

def draw_on_map(df, depot_count, task_count, vehicle_count, x, types, t):
# visualization : plotting with matplolib
    plt.figure(figsize=(8, 8))
    for i in range(depot_count):
        plt.scatter(df.longitude[i], df.latitude[i], c='green', s=100)
        plt.text(df.longitude[i], df.latitude[i], "depot_" + str(i), fontsize=12)


    for i in range(depot_count, task_count):
        plt.scatter(df.longitude[i], df.latitude[i], c=get_color_by_type(types[i]), s=10)
        plt.text(df.longitude[i], df.latitude[i], str(i) + " - " + types[i], fontsize=6)

    k0 = []
    k1 = []
    k2 = []
    k3 = []
    for k in range(vehicle_count):
        for i in range(task_count):
            for j in range(task_count):
                if i != j and pulp.value(x[i][j][k]) == 1:
                    if k == 0:
                        plt.plot([df.longitude[i], df.longitude[j]], [df.latitude[i], df.latitude[j]], c="green")
                        k0.append("%s_%s" % (i, j))
                    elif k == 1:
                        plt.plot([df.longitude[i], df.longitude[j]], [df.latitude[i], df.latitude[j]], c="red")
                        k1.append("%s_%s" % (i, j))
                    elif k == 2:
                        plt.plot([df.longitude[i], df.longitude[j]], [df.latitude[i], df.latitude[j]], c="gray")
                        k2.append("%s_%s" % (i, j))
                    elif k == 3:
                        plt.plot([df.longitude[i], df.longitude[j]], [df.latitude[i], df.latitude[j]], c="blue")
                        k3.append("%s_%s" % (i, j))
                    else:
                        plt.plot([df.longitude[i], df.longitude[j]], [df.latitude[i], df.latitude[j]], c="black")

    print("the array is: ", order_correctly(k0))
    print("the array is: ", order_correctly(k1))
    print("the array is: ", order_correctly(k2))
    print("the array is: ", order_correctly(k3))

    plt.show()