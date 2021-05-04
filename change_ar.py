import matplotlib.pyplot as plt

# 0.6 , 0.5, 0.3, 25, 50, 100
# 0.6 , 0.5, 0.3, 0.1 25, 50, 80, 120

def quality(c1, c2, T):
    t1 = c1.traj
    t2 = c1.traj
    t = range(T)
    k = "quality"
    plt.figure(figsize=(12,10))
    plt.subplot(2, 2, 1)
    plt.xlabel("year")
    plt.ylabel(k)
    line1, = plt.plot(range(0, 25), t2[k][:25], alpha=1, label="c1 ar = 0.7")
    line2, = plt.plot(range(24, 50), t2[k][24:50], alpha=1, label="c1 ar = 0.5")
    line3, = plt.plot(range(49, 80), t2[k][49:80], alpha=1, label="c1 ar = 0.3")
    line4, = plt.plot(range(79, T), t2[k][79:], alpha=1, label="c1 ar = 0.1")
    line5, = plt.plot(t, t1[k], alpha=1, label="c2 ar = " + str(c1.ar))
    plt.legend(handles=[line1, line2, line3, line4, line5])

    plt.subplot(2, 2, 2)
    k = "prestige"
    plt.xlabel("year")
    plt.ylabel(k)
    line1, = plt.plot(range(0, 25), t2[k][:25], alpha=1, label="c1 ar = 0.7")
    line2, = plt.plot(range(24, 50), t2[k][24:50], alpha=1, label="c1 ar = 0.5")
    line3, = plt.plot(range(49, 80), t2[k][49:80], alpha=1, label="c1 ar = 0.3")
    line4, = plt.plot(range(79, T), t2[k][79:], alpha=1, label="c1 ar = 0.1")
    line5, = plt.plot(t, t1[k], alpha=1, label="c2 ar = " + str(c1.ar))
    plt.legend(handles=[line1, line2, line3, line4, line5])

    plt.subplot(2, 2, 3)
    k = "num_of_paper"
    plt.xlabel("year")
    plt.ylabel(k)
    line1, = plt.plot(range(0, 25), t2[k][:25], alpha=1, label="c1 ar = 0.7")
    line2, = plt.plot(range(24, 50), t2[k][24:50], alpha=1, label="c1 ar = 0.5")
    line3, = plt.plot(range(49, 80), t2[k][49:80], alpha=1, label="c1 ar = 0.3")
    line4, = plt.plot(range(79, T), t2[k][79:], alpha=1, label="c1 ar = 0.1")
    line5, = plt.plot(t, t1[k], alpha=1, label="c2 ar = " + str(c1.ar))
    plt.legend(handles=[line1, line2, line3, line4, line5])

    plt.subplot(2, 2, 4)
    k = "author_res"
    plt.xlabel("year")
    plt.ylabel(k)
    line1, = plt.plot(range(0, 25), t2[k][:25], alpha=1, label="c1 ar = 0.7")
    line2, = plt.plot(range(24, 50), t2[k][24:50], alpha=1, label="c1 ar = 0.5")
    line3, = plt.plot(range(49, 80), t2[k][49:80], alpha=1, label="c1 ar = 0.3")
    line4, = plt.plot(range(79, T), t2[k][79:], alpha=1, label="c1 ar = 0.1")
    line5, = plt.plot(t, t1[k], alpha=1, label="c2 ar = " + str(c1.ar))
    plt.legend(handles=[line1, line2, line3, line4, line5])
    plt.show()


def components(c1, c2, T):
    # 0.7 0.6 0.5 0.4 0.3, 20, 60, 100, 140, 180
    t1 = c1.traj
    t2 = c2.traj
    t = range(T)
    k = "quality"

    plt.subplot(2, 2, 1)
    plt.xlabel("year")
    plt.ylabel(k)
    line1, = plt.plot(t, t1[k], alpha=1, label="ar = " + str(c1.ar))
    line2, = plt.plot(t, t2[k], alpha=1, label="ar = " + str(c2.ar))
    plt.legend(handles=[line1, line2])

    plt.subplot(2, 2, 2)
    k = "author_res"
    plt.xlabel("year")
    plt.ylabel(k)
    line1, = plt.plot(t, t1[k], alpha=1, label="ar = " + str(c1.ar))
    line2, = plt.plot(t, t2[k], alpha=1, label="ar = " + str(c2.ar))
    plt.legend(handles=[line1, line2])

    plt.subplot(2, 2, 3)
    k = "prestige"
    plt.xlabel("year")
    plt.ylabel(k)
    line1, = plt.plot(t, t1[k], alpha=1, label="ar = " + str(c1.ar))
    line2, = plt.plot(t, t2[k], alpha=1, label="ar = " + str(c2.ar))
    plt.legend(handles=[line1, line2])

    plt.subplot(2, 2, 4)
    k = "num_of_paper"
    plt.xlabel("year")
    plt.ylabel(k)
    line1, = plt.plot(t, t1[k], alpha=1, label="ar = " + str(c1.ar))
    line2, = plt.plot(t, t2[k], alpha=1, label="ar = " + str(c2.ar))
    plt.legend(handles=[line1, line2])
    plt.show()
