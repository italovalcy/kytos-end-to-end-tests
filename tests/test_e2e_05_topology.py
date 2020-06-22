import unittest
import requests
from tests.helpers import NetworkTest
import os
import signal
import time

CONTROLLER = '127.0.0.1'
KYTOS_API = 'http://%s:8181/api/kytos' % (CONTROLLER)


class TestE2ETopology(unittest.TestCase):
    def setUp(self):
        self.net = NetworkTest(CONTROLLER)
        self.net.start()
        self.net.wait_switches_connect()

    def tearDown(self):
        # This function tears down the whole topology.
        self.net.stop()
        # check all the logs on the end
        # TODO: persist the logs of syslog
        # TODO: multiple instances or single instance for checking memory leak / usage (benchmark - how many flows are supported? how many switches are supported?)
    def test_list_evcs_should_be_empty(self):
        """Test if list circuits return 'no circuit stored.'."""
        api_url = KYTOS_API+'/mef_eline/v2/evc/'
        response = requests.get(api_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})

    def test_list_switches(self):
        api_url = KYTOS_API+'/topology/v3/switches'
        response = requests.get(api_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue('switches' in data)
        self.assertEqual(len(data['switches']), 3)
        self.assertTrue('00:00:00:00:00:00:00:01' in data['switches'])
        self.assertTrue('00:00:00:00:00:00:00:02' in data['switches'])
        self.assertTrue('00:00:00:00:00:00:00:03' in data['switches'])

    def test_enabling_switch_persistent(self):
        sw1 = '00:00:00:00:00:00:00:01'
        sw2 = '00:00:00:00:00:00:00:02'
        sw3 = '00:00:00:00:00:00:00:03'

        # make sure the switches are disabled by default
        api_url = KYTOS_API+'/topology/v3/switches'
        response = requests.get(api_url)
        data = response.json()
        self.assertFalse(data['switches'][sw1]['enabled'])
        self.assertFalse(data['switches'][sw2]['enabled'])
        self.assertFalse(data['switches'][sw3]['enabled'])

        # enable the switches
        api_url = KYTOS_API+'/topology/v3/switches/%s/enable' % (sw1)
        response = requests.post(api_url)
        self.assertEqual(response.status_code, 201)
        api_url = KYTOS_API+'/topology/v3/switches/%s/enable' % (sw2)
        response = requests.post(api_url)
        self.assertEqual(response.status_code, 201)
        api_url = KYTOS_API+'/topology/v3/switches/%s/enable' % (sw3)
        response = requests.post(api_url)
        self.assertEqual(response.status_code, 201)

        # check if the switches are now enabled
        api_url = KYTOS_API+'/topology/v3/switches'
        response = requests.get(api_url)
        data = response.json()
        self.assertTrue(data['switches'][sw1]['enabled'])
        self.assertTrue(data['switches'][sw2]['enabled'])
        self.assertTrue(data['switches'][sw3]['enabled'])

        # restart kytos and check if the switches are still enabled
        with open('/var/run/kytos/kytosd.pid', "r") as f:
            pid = int(f.read())
            os.kill(pid, signal.SIGTERM)
        time.sleep(5)
        os.system('kytosd &')
        self.net.wait_switches_connect()

        # restore the status
        api_url = KYTOS_API+'/topology/v3/restore'
        response = requests.get(api_url)
        self.assertEqual(response.status_code, 200)

        # check if the switches are still enabled and now with the links
        api_url = KYTOS_API+'/topology/v3/switches'
        response = requests.get(api_url)
        data = response.json()
        self.assertTrue(data['switches'][sw1]['enabled'])
        self.assertTrue(data['switches'][sw2]['enabled'])
        self.assertTrue(data['switches'][sw3]['enabled'])

    def test_disabling_switch_persistent(self)
        # TODO: 1) start kytosd -E; 2) disable a switch; 3) restart
        # kytos - kill kytos.pid && kytosd -E; 4) check if the switch
        # remain disabled
        self.assertTrue(True)

    def test_enabling_interface_persistent(self)
        sw1if1 = '00:00:00:00:00:00:00:01:1'
        sw2if1 = '00:00:00:00:00:00:00:02:1'

        # make sure the interfaces are disabled by default
        api_url = KYTOS_API+'/topology/v3/interfaces'
        response = requests.get(api_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['interfaces']), 10)
        self.assertFalse(data['interfaces'][sw1if1]['enabled'])
        self.assertFalse(data['interfaces'][sw2if1]['enabled'])

        # enable the interfaces
        api_url = KYTOS_API+'/topology/v3/interfaces/%s/enable' % (sw1if1)
        response = requests.post(api_url)
        self.assertEqual(response.status_code, 201)
        api_url = KYTOS_API+'/topology/v3/interfaces/%s/enable' % (sw2if1)
        response = requests.post(api_url)
        self.assertEqual(response.status_code, 201)

        # check if the interfaces are now enabled
        api_url = KYTOS_API+'/topology/v3/interfaces'
        response = requests.get(api_url)
        data = response.json()
        self.assertTrue(data['interfaces'][sw1if1]['enabled'])
        self.assertTrue(data['interfaces'][sw2if1]['enabled'])

        # restart kytos and check if the interfaces are still enabled
        with open('/var/run/kytos/kytosd.pid', "r") as f:
            pid = int(f.read())
            os.kill(pid, signal.SIGTERM)
        time.sleep(5)
        os.system('kytosd &')
        self.net.wait_interfaces_connect()

        # restore the status
        api_url = KYTOS_API+'/topology/v3/restore'
        response = requests.get(api_url)
        self.assertEqual(response.status_code, 200)

        # check if the interfaces are still enabled and now with the links
        api_url = KYTOS_API+'/topology/v3/interfaces'
        response = requests.get(api_url)
        data = response.json()
        self.assertTrue(data['interfaces'][sw1if1]['enabled'])
        self.assertTrue(data['interfaces'][sw2if1]['enabled'])

    def test_enabling_all_interfaces_persistent(self)
        # TODO: 1) start kytosd -E; 2) enable all interfaces; 3) restart
        # kytos - kill kytos.pid && kytosd -E; 4 check if all interfaces 
        # remain enabled
        self.assertTrue(True)

    def test_disabling_interface_persistent(self)
        # TODO: 1) start kytosd -E; 2) disable a interface; 3) restart
        # kytos - kill kytos.pid && kytosd -E; 4 check if the interface 
        # remain disabled
        self.assertTrue(True)

    def test_disabling_all_interfaces_persistent(self)
        # TODO: 1) start kytosd -E; 2) disable all interfaces; 3) restart
        # kytos - kill kytos.pid && kytosd -E; 4 check if all interfaces 
        # remain disabled
        self.assertTrue(True)

    def test_enabling_link_persistent(self)
        endpoint_a = '00:00:00:00:00:00:00:01:2'
        endpoint_b = '00:00:00:00:00:00:00:02:2'

        # make sure the links are disabled by default
        api_url = KYTOS_API+'/topology/v3/links'
        response = requests.get(api_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['links']), 3)
        link_id1 = None
        for k,v in data['links'].items():
            if set([v['endpoint_a'], v['endpoint_b']]) == set([endpoint_a, endpoint_b]):
                link_id1 = k
        self.assertNotEqual(link_id1, None)
        self.assertFalse(data['links'][link_id1]['enabled'])

        # enable the links
        api_url = KYTOS_API+'/topology/v3/links/%s/enable' % (link_id1)
        response = requests.post(api_url)
        self.assertEqual(response.status_code, 201)

        # check if the links are now enabled
        api_url = KYTOS_API+'/topology/v3/links'
        response = requests.get(api_url)
        data = response.json()
        self.assertTrue(data['links'][link_id1]['enabled'])

        # restart kytos and check if the links are still enabled
        with open('/var/run/kytos/kytosd.pid', "r") as f:
            pid = int(f.read())
            os.kill(pid, signal.SIGTERM)
        time.sleep(5)
        os.system('kytosd &')
        self.net.wait_links_connect()

        # restore the status
        api_url = KYTOS_API+'/topology/v3/restore'
        response = requests.get(api_url)
        self.assertEqual(response.status_code, 200)

        # check if the links are still enabled and now with the links
        api_url = KYTOS_API+'/topology/v3/links'
        response = requests.get(api_url)
        data = response.json()
        self.assertTrue(data['links'][link_id1]['enabled'])

    def test_disabling_link_persistent(self)
        # TODO: 1) start kytosd -E; 2) disable the link1; 3) restart
        # kytos - kill kytos.pid && kytosd -E; 4 check if the link1
        # remain disabled
        self.assertTrue(True)

#    def test_all_enabled_should_activate_topology_discovery(self)
#        # /api/kytos/topology/v3/switches --> check if it is disabled
#        # /v3/switches/{dpid}/enable
#        # /api/kytos/topology/v3/switches --> check if it is enabled
#        # kill kytosd and restart, check if switches are still enabled
#        # check topology discovery

#    def test_basic_mef_eline(self):
#        # create a simple EVC intra-switch
#        # patch the EVC with new name
#        # patch the EVC with new UNIs
#        # Disable EVC
#        # Enable EVC