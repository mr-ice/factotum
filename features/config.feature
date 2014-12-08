Feature: factotum is configured by a yaml configuration file

  Scenario: The configuration file should load
    Given that we have a configuration file name
    When we try to load the configuration file
    Then the configuration file should load

  Scenario: config['actions'] is a dict
  Scenario: config['banner'] is a string
  Scenario: config['interface'] is a dotted-quad ip address
  Scenario: config['logging'] is a dict
  Scenario: config['port'] is an integer
  Scenario: config['version'] is digits and periods
  Scenario: config['client'] is a dict
  Scenario: config['actions'][$key] is a dict
  Scenario: config['actions'][$key]['environment'] is a list
  Scenario: config['actions'][$key]['chdir'] is a path
  Scenario: config['actions'][$key]['description'] is a string
  Scenario: config['actions'][$key]['exec'] is a string
  Scenario: config['actions'][$key]['return'] is from ('stdout','stderr','code')
  Scenario: config['actions'][$key]['return'] is from ('raw','json','yaml','xml')
  Scenario: config['logging']['facility'] is from ('user','
  Scenario: config['logging']['level'] is from ('emergency','alert','critical','error','warning','notice','info','debug')
  Scenario: config['logging']['file'] is a writable file
  Scenario: config['logging']['type'] is from ('file','syslog')
  Scenario: config['client']['version'] is a re
  Scenario: config['client']['verify'] is from (True,False)
  Scenario: config['client']['ip'] is a dotted-quad ip address or null

