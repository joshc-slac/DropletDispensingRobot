import json
import time
import random

from drops.DropsDriver import myClient
from drops.helpers.JsonFileHandler import JsonFileHandler
from drops.helpers.ServerResponse import ServerResponse
from TestHILDO import busy_wait

# pytest encourages this pattern, apologies.
ip = "172.21.148.101"
port = 9999
supported_json = "drops/supported.json"
client = myClient(ip=ip, port=port, supported_json=supported_json, reload=False)

# create config parser handler
json_handler = JsonFileHandler(supported_json)
# load configs and launch web server
json_handler.reload_endpoints()


class Test_HIL():

  def test_disconnect(self, capsys):
    resp = client.disconnect()
    assert resp.RESULTS == "Accepted"

  def test_connect(self, capsys):
    # TEST Connect
    client.disconnect()
    time.sleep(0.5)  # WAIT For Robot to not be Busy (500)
    resp = client.connect("BOB")
    assert resp.RESULTS == "Accepted"

#    Class 2 Test
  def test_get_status(self, capsys):
    # Checks if response looks like what we expect a status response should
    # look like
    resp = client.get_status()
    expected_keys = [
        'Position',
        'LastProbe',
        'Humidity',
        'Temperature',
        'BathTemp',
    ]
    assert expected_keys == list(resp.RESULTS.keys())

  def test_get_position_names(self, capsys):
    r = client.get_position_names()
    assert r.ERROR_CODE == 0


  def test_get_current_position(self, capsys):
    '''
       Checks if response looks like what we expect a status response should
       look like,

       Expected: name and properties of the last selected position,
                together with the real current position coordinates

        Currently only checks if a list is returned
    '''
    r = client.get_current_positions()
    expected_keys = [
            'CurrentPosition',
            'Position',
            'PositionReal',
            ]
    assert list(r.RESULTS.keys()) == expected_keys

  def test_get_task_names(self, capsys):
      # Check if reponse is not an empty array or any errors occured
    r = client.get_task_names()
    assert r.ERROR_CODE == 0

  def test_pulse_names(self, capsys):
    # Test if response is a list
    r = client.get_pulse_names()
    assert r.RESULTS != []

  def test_nozzle_status(self, capsys):
    # Test if repose has the expected keys

    r = client.get_nozzle_status()

    expected_keys = [
        "Activated Nozzles",
        "Selected Nozzles",
        "ID,Volt,Pulse,Freq,Volume",  # Intreseting? all one key
        "Trigger",
    ]
    assert list(r.RESULTS.keys()) == expected_keys

  def test_select_nozzle(self, capsys):
    '''
        Finds new active position using get_nozzle_status. Then selects new
        nozzle.

    '''
    # WAIT IF SERVER IS BUSY before starting new test
    # Might be a good header to keep in all tests.
    busy_wait(1)

    client.connect("Josue")
    r = client.get_nozzle_status()

    # Find active nozzle position
    activated_nozzles = list()
    for i, x in enumerate(r.RESULTS["Activated Nozzles"]):
      if x == True:
        activated_nozzles.append(i + 1)

    new_nozzle_pos = random.choice(activated_nozzles)
    r = client.select_nozzle(new_nozzle_pos)

    # Check if new Nozzle positoin was Accepted
    assert r.RESULTS == "Accepted"
    # Check if not active nozzle positoin is choosen the API reponds with Rject


  def test_set_led(self, capsys):
    '''
        Set LED to some value then turn off.

        Currently ther is no way to check LED value from the Robot
    '''

    busy_wait(1)
    # SET A VALUE
    r = client.setLED(1, 1)
    assert r.RESULTS == "Accepted"

    # OUT OF RANGE VALUE
    r = client.setLED(-1, -10)
    assert r.RESULTS == "Rejected"
    # Turn off?
    r = client.setLED(0, 1)
