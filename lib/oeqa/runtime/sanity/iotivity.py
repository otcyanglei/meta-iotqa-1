import os
import time
import string
from oeqa.oetest import oeRuntimeTest
from oeqa.utils.helper import shell_cmd_timeout
from oeqa.utils.helper import tag

@tag(TestType="Functional Positive", FeatureID="IOTOS-498")
class IOtvtClient(oeRuntimeTest):
    @classmethod
    def setUpClass(cls):
        '''Test simpleserver and simpleclient.'''
        cls.tc.target.run("killall simpleserver")
        cls.tc.target.run("killall simpleclient")
        # start server
        server_cmd = "/opt/iotivity/examples/resource/cpp/simpleserver > /tmp/svr_output &"
        (status, output) = cls.tc.target.run(server_cmd)
        time.sleep(1)
        # start client to get info
        client_cmd = "/opt/iotivity/examples/resource/cpp/simpleclient > /tmp/output &"
        cls.tc.target.run(client_cmd)
        print "\npatient... simpleclient needs long time for its observation"
        time.sleep(70)

    @classmethod
    def tearDownClass(cls):
        '''kill on Target'''
        cls.tc.target.run("killall simpleserver")
        cls.tc.target.run("killall simpleclient")

    def test_iotvt_findresource(self):
        '''Target finds resource, registered by Host'''
        (status, output) = self.target.run('cat /tmp/output')
        ret = 0
        if "DISCOVERED Resource" in output:
            pass
        else:
           ret = 1
        self.assertEqual(ret, 0, msg="Error messages: %s" % output)

    def test_iotvt_getstate(self):
        '''Target gets resource state'''
        (status, output) = self.target.run('cat /tmp/output')
        ret = 0
        if "GET request was successful" in output:
            pass
        else:
           ret = 1
        self.assertEqual(ret, 0, msg="Error messages: %s" % output)

    def test_iotvt_observer(self):
        '''Target sets observer'''
        (status, output) = self.target.run('cat /tmp/output')
        ret = 0
        if "Observe is used." in output and \
           "SequenceNumber: 14" in output:
            pass
        else:
           ret = 1
        self.assertEqual(ret, 0, msg="Error messages: %s" % output)

    def test_iotvt_setstate(self):
        '''Target sets resource state'''
        (status, output) = self.target.run('cat /tmp/output')
        ret = 0
        if "PUT request was successful" in output:
            pass
        else:
           ret = 1
        self.assertEqual(ret, 0, msg="Error messages: %s" % output)

    def test_iotvt_regresource(self):
        '''After several seconds, server should not crash'''
        time.sleep(2)
        # check if simpleserver is there
        (status, output) = self.target.run('ps | grep simpleserver -c')
        number = string.atoi(output)
        self.assertEqual(number, 3, msg="Error messages: %s" % output)
