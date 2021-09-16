from time import sleep
import sacn


DMX_OFFSET = 75

sender = sacn.sACNsender(
    fps=20,
)  # provide an IP-Address to bind to if you are using Windows and want to use multicast

sender.start()  # start the sending thread
sender.activate_output(1)  # start sending out data in the 1st universe
sender[1].multicast = False  # set multicast to False
sender[1].destination = "192.168.0.135"  # or provide unicast information.


def move_mirrors(m1, m2, m3, m4):
    sender[1].dmx_data = (
        *[0] * DMX_OFFSET,
        50,  # col
        m1[0],  # X-axis
        m1[1],  # Y-axis
        50,  # col
        m2[0],  # X-axis
        m1[1],  # Y-axis
        50,  # col
        m3[0],
        m3[1],
        50,
        m4[0],
        m4[1],
    )

def flint8(raw:float):
    result = 255 - int(min(255, max(0, raw * 255)))
    return result



if __name__ == "__main__":
    sleep(1)
    n = (128, 128)
    move_mirrors(n, n, n, n)

# ////////////

# sender[1].dmx_data = (*[0] * 75, 24, 128, 128)
# sleep(10)
# sender.stop()
# do not forget to stop the sender
