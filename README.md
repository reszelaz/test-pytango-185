# Test to validate PyTango#185

## Steps to reproduce

1. Create Tango DS's instance in the DB: 
```console
$> tango_admin --add-server DummyEventGenerator/test DummyEventGenerator test/dummyeventgenerator/1
```
2. Start the DS:
```console
$> python3 DummyEventGenerator.py test -v4
```
3. Start the client:
```console
$> python3 test_python_cb.py test/dummyeventgenerator/1 attr change 1
```
4. Start emitting events from the DS:
```console
$> python3 -c "import tango; tango.DeviceProxy('test/dummyeventgenerator/1').Start(0.1)"
```