from behave import *
import rtyaml

@given('that we have a configuration file name')
def step_have_config_file(context):
    if ( file('config.yaml')): pass

@when('we try to load the configuration file')
def step_try_to_load_config_files(context):
    context.config_content = rtyaml.load(file('config.yaml'))
    if (context.config_content ): pass

@then('the configuration file should load')
def step_load_config_file(context):
    if (isinstance(context.config_content,dict)): pass