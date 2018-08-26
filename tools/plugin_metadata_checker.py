#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2018-       Martin Sinn                         m.sinn@gmx.de
#########################################################################
#  This file is part of SmartHomeNG
#  https://github.com/smarthomeNG/smarthome
#  http://knx-user-forum.de/
#
#  SmartHomeNG is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHomeNG is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHomeNG. If not, see <http://www.gnu.org/licenses/>.
#########################################################################


"""
This script creates a list showing the care status of the metadata file
of the plugins on the .../plugins folder.

The result is printed to stdout
"""

import os
import argparse

print('')
print(os.path.basename(__file__) + ' - Checks the care status of plugin metadata')
print('')
start_dir = os.getcwd()

import sys
# find lib directory and import lib/item_conversion
os.chdir(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, '..')
sys.path.insert(0, '../lib')
import shyaml



type_unclassified = 'unclassified'
plugin_sections = [ ['gateway', 'Gateway', 'Gateway'],
                    ['interface', 'Interface', 'Interface'],
                    ['protocol', 'Protocol', 'Protokoll'],
                    ['system', 'System', 'System'],
                    [type_unclassified, 'Non classified', 'nicht klassifizierte'],
                    ['web', 'Web/Cloud', 'Web/Cloud']
                  ]


# ==================================================================================
#   Functions of the tool
#

def get_local_pluginlist():
    plglist = os.listdir('.')

    for entry in plglist:
        if entry[0] in ['.' ,'_'] or entry == 'deprecated_plugins':
            plglist.remove(entry)
    for entry in plglist:
        if entry[0] in ['.' ,'_']:
            plglist.remove(entry)
    for entry in plglist:
        if entry[0] in ['.' ,'_']:
            plglist.remove(entry)
    return plglist


def get_plugintype(plgName):

    fn = './'+plgName+'/__init__.py'
    try:
        with open(fn, "r") as myfile:
            code = myfile.read()
    except:
        return 'None' \
               ''
    if code.find('SmartPlugin') == -1:
        return 'Classic'
    return 'Smart'



def readMetadata(metaplugin, plugins_local):

    metafile = metaplugin + '/plugin.yaml'
    plg_dict = {}
    plugin_yaml = {}
    if metaplugin in plugins_local:  # pluginsyaml_local
        if os.path.isfile(metafile):
            plugin_yaml = shyaml.yaml_load(metafile, ordered=True)
    return plugin_yaml


# ==================================================================================
#   Functions to list plugin information
#

def list_formatted(plugin, plgvers, plgstate, plgtype, plgGlobal, plgParams, plgAttr, plgFunc=''):
    print('{plugin:<15.15} {plgvers:<8.8} {plgstate:<9.9} {plgtype:<8.8} {plgGlobal:<7.7} {plgParams:<8.8} {plgAttr:<8.8} {plgFunc:<9.9}'.format(plugin=plugin,
                                                                                                   plgvers=plgvers,
                                                                                                   plgstate=plgstate,
                                                                                                   plgtype=plgtype,
                                                                                                   plgGlobal=plgGlobal,
                                                                                                   plgParams=plgParams,
                                                                                                   plgAttr=plgAttr,
                                                                                                   plgFunc=plgFunc))

def list_plugins(option):

    option = option.strip().lower()

#    plugin_types = []
#    for pl in plugin_sections:
#        plugin_types.append(pl[0])

    plugins_local = get_local_pluginlist()

    header_displayed = False;
    plgcount = 0
    allplgcount = 0
    for plg in sorted(plugins_local):
        version = '-'
#        sectionPlg = '-'
        sectionParam = '-'
        sectionIAttr = '-'
        sectionFunc = '-'
        comment = ''
        metadata = readMetadata(plg, plugins_local)
        if metadata.get('plugin', None) == None:
            sectionPlg = 'No'
        else:
            sectionPlg = 'Ok'
            version = metadata['plugin'].get('version', '-')
            plgstate = metadata['plugin'].get('state', '-')
            if not plgstate in ['qa-passed', 'ready', 'develop', '-']:
                plgstate = 'INVALID'
        plgtype = get_plugintype(plg)
        if plgtype == 'Smart':
            if version == '-':
                version = '?'

            if metadata.get('parameters', None) == None:
                sectionParam = 'No'
            elif metadata.get('parameters', None) == 'NONE':
                sectionParam = 'Ok'
            else:
                sectionParam = 'Ok'
                sectionParam += ' (' + str(len(metadata['parameters'])) + ')'

            if metadata.get('item_attributes', None) == None:
                sectionIAttr = 'No'
            elif metadata.get('item_attributes', None) == 'NONE':
                sectionIAttr = 'Ok'
            else:
                sectionIAttr = 'Ok'
                sectionIAttr += ' (' + str(len(metadata['item_attributes'])) + ')'

            if metadata.get('plugin_functions', None) == None:
                sectionFunc = 'No'
            elif metadata.get('plugin_functions', None) == 'NONE':
                sectionFunc = 'Ok'
            else:
                sectionFunc = 'Ok'
                sectionFunc += ' (' + str(len(metadata['plugin_functions'])) + ')'

        if (option == 'all') or \
           (option == plgtype.lower()) or \
           (option == 'inc' and (sectionPlg == 'No' or sectionParam == 'No' or sectionIAttr == 'No' or sectionFunc == 'No')) or \
           (option == 'compl' and (plgtype.lower() != 'classic' and sectionPlg != 'No' and sectionParam != 'No' and sectionIAttr != 'No' and sectionFunc != 'No')) or \
           (option == 'inc_para' and sectionParam == 'No') or (option == 'inc_attr' and sectionIAttr == 'No'):
            if not header_displayed:
                ul = '-------------------------------'
                list_formatted('', '', '', 'Plugin', '', 'Plugin', 'Item', 'Plugin')
                list_formatted('Plugin', 'Version', 'State', 'Type', 'Info', 'Params', 'Attrib.', 'Functions')
                list_formatted(ul, ul, ul, ul, ul, ul, ul, ul)
                header_displayed = True
            list_formatted(plg, version, plgstate, plgtype, sectionPlg, sectionParam, sectionIAttr, sectionFunc)
            plgcount += 1
        allplgcount += 1
    print()
    if (option == 'all'):
        print("{} plugins".format(plgcount))
    else:
        print("{} plugins of {} plugins total".format(plgcount, allplgcount))
    print()
    return


# ==================================================================================
#   Functions to display information of one plugin
#

def disp_formatted(lbl, val):
    val = val.replace('\n', ' ')
    print('{lbl:<18.18} {val:<55.55}'.format(lbl=lbl, val=val))
    while len(val) > 55:
        val = val[55:]
        print('{lbl:<18.18} {val:<55.55}'.format(lbl='', val=val))


def disp_formatted2(lbl, typ, val=''):
    print('{lbl:<19.19}{typ:<12.12} {val:<48.48}'.format(lbl=lbl, typ=typ, val=val))
    while len(val) > 48:
        val = val[48:]
        print('{lbl:<19.19}{typ:<13.13}{val:<48.48}'.format(lbl='', typ='', val=val))


def display_definition(name, dict):

    val = ''
    val2 = ''
    if dict.get('mandatory', False) == True:
        val += 'Mandatory'
    if dict.get('default', None) != None:
        if val != '':
            val += ', '
        if dict.get('default', None) == 'None*':
            val += "default=None"
        else:
            val += "default='" + str(dict.get('default', None)) + "'"
    if dict.get('valid_min', None) != None:
        if val != '':
            val += ', '
        val += "valid_min='" + str(dict.get('valid_min', None)) + "'"
    if dict.get('valid_max', None) != None:
        if val != '':
            val += ', '
        val += "valid_max='" + str(dict.get('valid_max', None)) + "'"
    if dict.get('valid_list', None) != None:
        if val != '':
            val += ', '
        val += "valid_list=" + str(dict.get('valid_list', None))
    disp_formatted2(name, dict.get('type', 'foo'), val)


def display_def_description(name, dict):
    if name != '':
        print(name)
    if dict.get('description', None) != None:
        disp_formatted('- Description (DE)', dict['description'].get('de', '-'))
        disp_formatted('- Description (EN)', dict['description'].get('en', '-'))


def display_metadata(plg, with_description):

    plg_type = get_plugintype(plg)
    print("Display metadata for {} plugin '{}'".format(plg_type, plg))
    print()
    plugins_local = get_local_pluginlist()
    metadata = readMetadata(plg, plugins_local)

    if metadata.get('plugin', None) == None:
        print("ERROR: Section 'plugin' not defined in metadata")
        print()
    else:
        if metadata['plugin'].get('description', None) != None:
            disp_formatted('Description (DE)', metadata['plugin']['description'].get('de', '-'))
            disp_formatted('Description (EN)', metadata['plugin']['description'].get('en', '-'))
            print()

        disp_formatted('Version', metadata['plugin'].get('version', '-'))
        disp_formatted('State', metadata['plugin'].get('state', '-'))
        disp_formatted('Type', metadata['plugin'].get('type', '-'))
        disp_formatted('Multi Instance', str(metadata['plugin'].get('multi_instance', '-')))
        disp_formatted('Restartable', str(metadata['plugin'].get('restartable', '-')))
        disp_formatted('shNG min. Version', str(metadata['plugin'].get('sh_minversion', '-')))
        disp_formatted('shNG max. Version', str(metadata['plugin'].get('sh_maxversion', '-')))
        disp_formatted('Classname', metadata['plugin'].get('classname', '-'))

        disp_formatted('Maintainer', metadata['plugin'].get('maintainer', '-'))
        disp_formatted('Tester', metadata['plugin'].get('tester', '-'))
        disp_formatted('Keywords', metadata['plugin'].get('keywords', '-'))
        disp_formatted('Documentation', metadata['plugin'].get('documentation', '-'))
        disp_formatted('Support', metadata['plugin'].get('support', '-'))
        print()



    if plg_type == 'Classic':
        return

    if metadata.get('parameters', None) == None:
        print("ERROR: Section 'parameters' not defined in metadata")
        print()
    elif metadata.get('parameters', None) == 'NONE':
        print("Parameters")
        print("----------")
        print("No parameters defined for this plugin")
        print()
    else:
        print("Parameters")
        print("----------")
        for par in metadata.get('parameters', None):
            par_dict = metadata['parameters'][par]
            display_definition(par, par_dict)
        print()
        if with_description:
            for par in metadata.get('parameters', None):
                par_dict = metadata['parameters'][par]
                display_def_description(par, par_dict)
            print()

    if metadata.get('item_attributes', None) == None:
        print("ERROR: Section 'item_attributes' not defined in metadata")
        print()
    elif metadata.get('item_attributes', None) == 'NONE':
        print("Item Attributes")
        print("---------------")
        print("No item attributes defined for this plugin")
        print()
    else:
        print("Item Attributes")
        print("---------------")
        for attr in metadata.get('item_attributes', None):
            attr_dict = metadata['item_attributes'][attr]
            display_definition(attr, attr_dict)
        print()
        if with_description:
            for attr in metadata.get('item_attributes', None):
                attr_dict = metadata['item_attributes'][attr]
                display_def_description(attr, attr_dict)
            print()

    if metadata.get('plugin_functions', None) == None:
        print("ERROR: Section 'plugin_functions' not defined in metadata")
        print()
    elif metadata.get('plugin_functions', None) == 'NONE':
        print("Plugin Functions")
        print("----------------")
        print("No functions have been defined for this plugin")
        print()
    else:
        print("Plugin Functions")
        print("----------------")
        for func in metadata.get('plugin_functions', None):
            func_dict = metadata['plugin_functions'][func]
            display_definition(func, func_dict)
            if with_description:
                display_def_description('', func_dict)
            if func_dict.get('parameters', None) != None:
                print("Parameters:")
                for param in func_dict.get('parameters', None):
                    param_dict = func_dict['parameters'][param]
                    display_definition(param, param_dict)
                    if with_description:
                        if param_dict.get('description', None) != None:
                            disp_formatted('- Description (DE)', param_dict['description'].get('de', '-'))
                            disp_formatted('- Description (EN)', param_dict['description'].get('en', '-'))
            print()
        print()

    return


# ==================================================================================
#   Functions to check the information of one plugin
#

errors = 0
warnings = 0
hints = 0

def disp_error_formatted(level, msg):
    if level != '':
        level += ':'
    print('{level:<8.8} {msg:<65.65}'.format(level=level, msg=msg))
    while len(msg) > 65:
        msg = msg[65:]
        print('{level:<8.8} {msg:<65.65}'.format(level='', msg=msg))
    return


def disp_hints_formatted(hint, hint2):
    if hint != '':
        print()
        disp_error_formatted('', hint)
        if hint2 != '':
            print()
            disp_error_formatted('', hint2)
        print()


def disp_error(msg, hint='', hint2=''):
    global errors
    errors += 1
    disp_error_formatted('ERROR', msg)
    disp_hints_formatted(hint, hint2)
    return


def disp_warning(msg, hint='', hint2=''):
    global warnings
    warnings += 1
    disp_error_formatted('WARNING', msg)
    disp_hints_formatted(hint, hint2)
    return


def disp_hint(msg, hint='', hint2=''):
    global hints
    hints += 1
    disp_error_formatted('HINT', msg)
    disp_hints_formatted(hint, hint2)
    return



def check_metadata(plg, with_description):

    plg_type = get_plugintype(plg)
    print("Check metadata of {} plugin '{}'".format(plg_type, plg))
    print()
    plugins_local = get_local_pluginlist()
    metadata = readMetadata(plg, plugins_local)

    # Checking global metadata
    if metadata.get('plugin', None) == None:
        disp_error("No global metadata defined", "Make sure to create a section 'plugin' and fill it with the necessary entries", "Take a look at https://www.smarthomeng.de/developer/development_plugin/plugin_metadata.html")
    else:
        if metadata['plugin'].get('version', None) == None:
            disp_error('No version number given', "Add 'version:' to the plugin section")
        if metadata['plugin'].get('state', None) == None:
            disp_error('No development state given for the plugin', "Add 'state:' to the plugin section and set it to one of the following values ['develop', 'ready', 'qa-passed']", "The state'qa-passed' should only be set by the shNG core team")
        if metadata['plugin'].get('classname', None) == None:
            disp_error('No classname for the plugin', "Add 'classname:' to the plugin section and set it to the name of the Python class that implements the plugin")

        if metadata['plugin'].get('type', None) == None:
            disp_warning('No plugin type set', "Add 'type:' to the plugin section")
        if metadata['plugin'].get('maintainer', None) == None:
            disp_warning('The maintainer of the plugin is not documented', "Add 'maintainer:' to the plugin section")
        if metadata['plugin'].get('multi_instance', None) == None:
            disp_warning('It is not documented if wether the plugin is multi-instance capable or not', "Add 'multi_instance:' to the plugin section")
        else:
            if not(metadata['plugin'].get('multi_instance', None) in [True, False]):
                disp_error('multi_instance has to be True or False')
        if metadata['plugin'].get('restartable', None) == None:
            disp_hint('It is not documented if wether the plugin is restartable or not [stop() and run()]', "Add 'restartable:' to the plugin section")
        else:
            if not(metadata['plugin'].get('restartable', None) in [True, False, 'True', 'False', 'unknown']):
                disp_error('restartable has to be True, False or unknown')
        if metadata['plugin'].get('sh_minversion', None) == None:
            disp_warning('No minimum version of the SmartHomeNG core given that is needed to run the plugin', "Add 'sh_minversion:' to the plugin section")

        if metadata['plugin'].get('tester', None) == None:
            disp_hint('The tester(s) of the plugin are not documented', "Add 'tester:' to the plugin section")


    # Checking parameter metadata
    if metadata.get('parameters', None) == None:
        disp_error("No parameters defined in metadata", "When defining parameters, make sure that you define ALL parameters of the plugin, but dont define global parameters like 'instance'. If only a part of the parameters are defined in the metadata, the missing parameters won't be handed over to the plugin at runtime.", "If the plugin has no parameters, document this by writing 'parameters: NONE' to the metadata file.")


    # Checking item attribute metadata
    if metadata.get('item_attributes', None) == None:
        disp_error("No item attributes defined in metadata", "If the plugin defines no item attributes, document this by creating an empty section. Write 'item_attributes: NONE' to the metadata file.")


    # Checking function metadata
    if metadata.get('plugin_functions', None) == None:
        disp_error("No public functions of the attribute defined in metadata", "If the plugin defines no public functions, document this by creating an empty section. Write 'plugin_functions: NONE' to the metadata file.")

    # Checking if the descriptions are complete
    if metadata.get('plugin', None) != None:
        if metadata['plugin'].get('description', None) == None:
            de = ''
            en = ''
        else:
            de = metadata['plugin']['description'].get('de', None)
            en = metadata['plugin']['description'].get('en', None)
        if de == None and en == None:
            disp_error('No description of the plugin is given', "Add the section 'description:' to the plugin section and fill the needed values")
        else:
            if de == None:
                disp_warning('No german description of the plugin is given', "Add 'de:' to the description section of the plugin section")
            if en == None:
                disp_warning('No english description of the plugin is given', "Add 'en:' to the description section of the plugin section")

    if metadata.get('parameters', None) != None:
        if metadata.get('parameters', None) != 'NONE':
            for par in metadata.get('parameters', None):
                par_dict = metadata['parameters'][par]
                if par_dict.get('description', None) == None:
                    de = ''
                    en = ''
                else:
                    de = par_dict['description'].get('de', '')
                    en = par_dict['description'].get('en', '')
                if de == '' and en == '':
                    disp_error("No description of the parameter '"+par+"' is given", "Add the section 'description:' to the parameter's section and fill the needed values")
                else:
                    if de == '':
                        disp_warning("No german description of the parameter '" + par + "' is given",
                                   "Add 'de:' to the description section of the parameter")
                    if en == '':
                        disp_warning("No english description of the parameter '" + par + "' is given",
                                   "Add 'en:' to the description section of the parameter")

    if metadata.get('item_attributes', None) != None:
        if metadata.get('item_attributes', None) != 'NONE':
            for par in metadata.get('item_attributes', None):
                par_dict = metadata['item_attributes'][par]
                if par_dict.get('description', None) == None:
                    de = ''
                    en = ''
                else:
                    de = par_dict['description'].get('de', '')
                    en = par_dict['description'].get('en', '')
                if de == '' and en == '':
                    disp_error("No description of the item attribute '"+par+"' is given", "Add the section 'description:' to the item attributes's section and fill the needed values")
                else:
                    if de == '':
                        disp_warning("No german description of the item attribute '" + par + "' is given",
                                   "Add 'de:' to the description section of the item attribute")
                    if en == '':
                        disp_warning("No english description of the item attribute '" + par + "' is given",
                                   "Add 'en:' to the description section of the item attribute")

    if metadata.get('plugin_functions', None) != None:
        if metadata.get('plugin_functions', None) != 'NONE':
            for func in metadata.get('plugin_functions', None):
                func_dict = metadata['plugin_functions'][func]
                if func_dict.get('description', None) == None:
                    de = ''
                    en = ''
                else:
                    de = func_dict['description'].get('de', '')
                    en = func_dict['description'].get('en', '')
                if de == '' and en == '':
                    disp_error("No description of the plugin function '"+func+"' is given", "Add the section 'description:' to the plugin function's section and fill the needed values")
                else:
                    if de == '':
                        disp_warning("No german description of the plugin function '" + func + "' is given",
                                   "Add 'de:' to the description section of the plugin function")
                    if en == '':
                        disp_warning("No english description of the plugin function '" + func + "' is given",
                                   "Add 'en:' to the description section of the plugin function")

                # Check function parameters
                if func_dict.get('parameters', None) != None:
                    for par in func_dict.get('parameters', None):
                        par_dict = func_dict['parameters'][par]
                        if par_dict.get('description', None) == None:
                            de = ''
                            en = ''
                        else:
                            de = par_dict['description'].get('de', '')
                            en = par_dict['description'].get('en', '')
                        if de == '' and en == '':
                            disp_warning("No description of the parameter '"+par+"' of plugin function '"+func+"' is given", "Add the section 'description:' to the plugin function's parameter section and fill the needed values")
                        else:
                            if de == '':
                                disp_warning("No german description of the parameter '" + par + "' of the function '"+func+"' is given",
                                           "Add 'de:' to the description section of the plugin function's parameter")
                            if en == '':
                                disp_warning("No english description of the parameter '" + par + "' of the function '"+func+"' is given",
                                           "Add 'en:' to the description section of the plugin function's parameter")

    global errors, warnings, hints
    if errors == 0 and warnings == 0 and hints == 0:
        print("Metadata is complete ({} errors, {} warnings and {} hints)".format(errors, warnings, hints))
    else:
        print("{} errors, {} warnings and {} hints".format(errors, warnings, hints))
    print()
    return


# ==================================================================================
#   Main Routine of the tool
#

if __name__ == '__main__':

    # change the working diractory to the directory from which the converter is loaded (../tools)
    os.chdir(os.path.dirname(os.path.abspath(os.path.basename(__file__))))

    plugindirectory = '../plugins'
    pluginabsdirectory = os.path.abspath(plugindirectory)

    os.chdir(pluginabsdirectory)

    parser = argparse.ArgumentParser(add_help=False)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-la', '--list_all', action="store_true", default=False, help='list plugin information of all plugins')
    group.add_argument('-lcl', '--list_classic', action="store_true", default=False, help='list plugin information of classic plugins')
    group.add_argument('-lsm', '--list_smart', action="store_true", default=False, help='list plugin information of smart plugins')
    group.add_argument('-li', '--list_inc', action="store_true", default=False, help='list information of plugins with incomplete metadata')
    group.add_argument('-lc', '--list_compl', action="store_true", default=False, help='list information of plugins with complete metadata')
    group.add_argument('-lip', action="store_true", default=False, help='list info of plugins with incomplete parameter data')
    group.add_argument('-lia', action="store_true", default=False, help='list info of plugins with incomplete item attribute data')
    group.add_argument('-d', dest='disp_plugin', help='display the metadata of a plugin')
    group.add_argument('-dd', dest='dispd_plugin', help='display the metadata of a plugin with description')
    group.add_argument('-c', dest='check_plugin', help='check the metadata of a plugin')
    args = parser.parse_args()

    try:
        if args.list_all:
            list_plugins('all')
        elif args.list_classic:
            list_plugins('classic')
        elif args.list_smart:
            list_plugins('smart')
        elif args.list_inc:
            list_plugins('inc')
        elif args.list_compl:
            list_plugins('compl')
        elif args.lip:
            list_plugins('inc_para')
        elif args.lia:
            list_plugins('inc_attr')
        elif args.disp_plugin:
            display_metadata(args.disp_plugin, False)
        elif args.dispd_plugin:
            display_metadata(args.dispd_plugin, True)
        elif args.check_plugin:
            check_metadata(args.check_plugin, False)
        else:
            parser.print_help()
            print()
    except ValueError as e:
        print("")
        print(e)
        print("")
        parser.print_help()
        print()
        exit(1)