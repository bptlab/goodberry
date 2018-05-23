#!/usr/bin/env python
from device import Device
import utils
from utils import DeviceArtifact
from component.components import Components

"""
This script handles the device setup.
"""

DEVICE_NAME_REGEX = "^[a-zA-Z0-9_\-\.\!\~\*\'\(\)]*$"
FEATURE_PROPERTY_REGEX = "^[_a-zA-Z][_a-zA-Z0-9\-]*$"


def request_device_name():
    """
    Asks the user for a device name. The name has to consist of URI
    allowed characters only (http://www.ietf.org/rfc/rfc2396.txt).
    :return: uri conform string
    :rtype: str
    """
    raw_name = input("Please choose a name for your new device:\n")
    return utils.input_require_match_reqex(DEVICE_NAME_REGEX, raw_name)


def setup_artifact(artifact, parent_artifact=None):
    """
    Lets the user setup (name) a new artifact (an artifact can be anything from the DeviceArtifact-enum defined in utils).
    :param artifact: kind of artifact to setup
    :type artifact: a DeviceArtifact-enum element
    :param parent_artifact: name of the artifact of higher order
    :type parent_artifact: str
    :return: name of the configured artifact
    :rtype: str
    """
    name = input("Please name the new " + artifact.name + ":\n")
    name = utils.input_require_match_reqex(FEATURE_PROPERTY_REGEX, name)
    device.add_artifact(artifact, name, parent_artifact)
    return name


def choose_feature():
    """
    Offers the user a list of feature-names so he can choose one.
    The user can also add a new feature and select this feature, instead of an already existing one.
    :return: name of the selected feature
    :rtype: str
    """
    features = device.get_list_of_features()
    print("Please select a feature to insert the component:")
    feature_id = utils.ask_choose_index_from_list_or_new(features)
    if feature_id is None:
        return setup_artifact(DeviceArtifact.Feature)
    return features[feature_id]


def setup_component():
    """
    Shows a list of available components to the user and lets the user choose and configure one component.
    :return: None
    :rtype: None
    """
    print("Please choose a component to be added to your device:")
    component = utils.ask_choose_from_enum(Components)

    # Each component can be an action, observer or even both.
    # As we can not be sure which combination it is, we use the pythonic way of exceptions in the following.
    # Try to execute config method for observer-component
    try:
        config_method = component.value.configure_observer
    except AttributeError:
        pass
    else:
        feature_name = choose_feature()
        property_name = setup_artifact(DeviceArtifact.Property, feature_name)
        property_config = config_method()
        property_config["type"] = component.name
        device.set_property_config(feature_name, property_name, property_config)
    # Try to execute config method for action-component
    try:
        config_method = component.value.configure_action
    except AttributeError:
        pass
    else:
        action_name = setup_artifact(DeviceArtifact.Action)
        action_config = config_method()
        action_config["type"] = component.name
        device.set_action_config(action_name, action_config)

    print("Completed setup for " + component.name + " component.\n")


def setup_new_device():
    """
    Starts the setup procedure for a new device.
    The device that is configured, is saved as a module global variable.
    :return: None
    :rtype: None
    """
    print("The following steps will guide you through the setup of your new raspberry device.")
    device.name = request_device_name()
    print("Your device id is \"" + device.id + "\".")
    should_add_component = True
    while should_add_component:
        setup_component()
        should_add_component = utils.ask_yes_no_question("\nAdd another component?")


def main():
    """
    This methods leads through the whole setup process for a device.
    After the setup, the user is asked, if the configuration should be saved to disk (necessary for running the device).
    :return: None
    :rtype: None
    """
    global device
    device = Device()
    print("Welcome to goodberry.")
    if utils.settings_exist():
        print("An existing settings file was found.")
        if utils.ask_yes_no_question("Do you want to import it?"):
            device.load_settings()
            print("Successfully loaded settings for device " + device.name)
        else:
            print("Please keep in mind, that your existing settings will be overwritten.")
            setup_new_device()
    else:
        setup_new_device()

    print("You finished the setup.")

    if utils.ask_yes_no_question("Do you want to save your current settings?"):
        device.write_settings()
        print("Wrote settings to disk.")
    print("Bye.")


if __name__ == "__main__":
    main()
