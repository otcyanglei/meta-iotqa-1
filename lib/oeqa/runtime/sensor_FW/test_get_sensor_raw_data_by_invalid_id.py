'''Verify get sensor raw data failed if id is invalid'''
import os
from oeqa.utils.helper import get_files_dir
import readConfigFile
from oeqa.oetest import oeRuntimeTest

class TestGetSensorRawDataByInvalidID(oeRuntimeTest):
    '''Verify error returned if sensor id is invalid'''
    def testGetSensorRawDataByInvalidID(self):
        '''Verify error returned if sensor id is invalid'''      
        mkdir_path = "mkdir -p /opt/sensor-test/apps/"
        (status, output) = self.target.run(mkdir_path)
        copy_path = os.path.join(get_files_dir(), 'test_get_sensor_raw_data_by_id')
        (status, output) = self.target.copy_to(copy_path, \
"/opt/sensor-test/apps/")
        #run test get sensor raw data by invalid id and show it's information
        client_cmd = "/opt/sensor-test/apps/test_get_sensor_raw_data_by_id " \
                     + readConfigFile.ReadConfFile.getSectionValue( 'sensors','invalid-id')
        (status, output) = self.target.run(client_cmd)
        print output
        self.assertEqual(status, 0, msg="Error messages: %s" % output)