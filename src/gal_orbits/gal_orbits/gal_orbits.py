import rclpy
from rclpy.node import Node

import numpy as np
import pandas as pd
from std_msgs.msg import Float64MultiArray
import gal_orb.GalOrb_bar as gal
from astropy.coordinates import SkyCoord, ICRS, Galactic
import astropy.units as u

class gal_orbits(Node):

    def __init__(self):
        super().__init__('gal_orbits')

        self.publish = self.create_publisher(Float64MultiArray , '/gal_orbits', 10)

        self.declare_parameter('rh', 0.0)
        self.declare_parameter('lon', 0.0)
        self.declare_parameter('lat', 0.0)
        self.declare_parameter('vr', 0.0)
        self.declare_parameter('pmra', 0.0)
        self.declare_parameter('pmde', 0.0)
        self.declare_parameter('t0', 0.0)
        self.declare_parameter('tf', 0.0)
        self.declare_parameter('M_disc', 100.0)
        self.declare_parameter('M_sph', 30.0)
        self.declare_parameter('reverse', 'False')
        self.declare_parameter('rtol', 1e-9)
        self.declare_parameter('atol', 1e-9)

        rh = self.get_parameter('rh').get_parameter_value().double_value
        lon = self.get_parameter('lon').get_parameter_value().double_value
        lat = self.get_parameter('lat').get_parameter_value().double_value
        vr = self.get_parameter('vr').get_parameter_value().double_value
        pmra = self.get_parameter('pmra').get_parameter_value().double_value
        pmde = self.get_parameter('pmde').get_parameter_value().double_value
        t0 = self.get_parameter('t0').get_parameter_value().double_value
        tf = self.get_parameter('tf').get_parameter_value().double_value
        M_disc = self.get_parameter('M_disc').get_parameter_value().double_value
        M_sph = self.get_parameter('M_sph').get_parameter_value().double_value
        reverse = self.get_parameter('reverse').get_parameter_value().string_value
        rtol = self.get_parameter('rtol').get_parameter_value().double_value
        atol = self.get_parameter('atol').get_parameter_value().double_value
        if reverse == 'True':
            reverse_bool = True
        else:
            reverse_bool = False

        icrs_coords = Galactic(l=lon * u.deg, b=lat * u.deg).transform_to(ICRS())

        sc = SkyCoord(icrs_coords.ra, icrs_coords.dec, pm_ra_cosdec=pmra*u.mas/u.yr, pm_dec=pmde*u.mas/u.yr)

        pml = sc.galactic.pm_l_cosb.value
        pmb = sc.galactic.pm_b.value

        self.get_logger().info(f"Starting gal_orbits")

        F = gal.gal_orb(rh, lon, lat, vr, pml, pmb, t0, tf, M_disc = M_disc, M_sph = M_sph, name = None,
                    reverse = reverse_bool, rtol=rtol, atol=atol, plot = False, output = False)
        if len(F) == 0:
            self.get_logger().info(f"there is no data in the output")

        self.data_length = len(F)
        self.all_columns = ['t', 'R', 'Vr', 'fi', 'Vfi', 'z', 'Vz', 'E', 'C', 'xg', 'yg']

        self.publish_msg = Float64MultiArray()
        self.float_arrays = F.to_numpy()
        
        #Defining inputs
        self.declare_parameter('publish_freq', 10.0)   

        # Defining encounter for publisher
        self.i = 0

        timer_period = 1/self.get_parameter('publish_freq').get_parameter_value().double_value  # frequency of publishing
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
    def timer_callback(self):

        self.publish_msg.data = [float(self.float_arrays[self.i][j]) for j in range(len(self.float_arrays[0]))]

        self.publish.publish(self.publish_msg)

        # self.get_logger().info(f"Publishing via self.pos_GT_pub = {self.publish_msg.data}")

        self.i += 1
        if self.i==self.data_length:
            self.get_logger().info('All data published successfully')
            exit()

        
def main(args=None):
    rclpy.init(args=args)
    dynamics = gal_orbits()
    rclpy.spin(dynamics)
    dynamics.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()