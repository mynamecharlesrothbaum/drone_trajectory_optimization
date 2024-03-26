from sitl_controller import SitlController
import time


def main():
    sim = SitlController
    if(sim.start_new_instance):
        print("it worked")


if __name__ == "__main__":
    main()