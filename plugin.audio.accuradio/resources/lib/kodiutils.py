#/*
# *
# * TuneIn Radio for Kodi.
# *
# * Copyright (C) 2015 Brian Hornsby
# *
# * This program is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *
# */


def check_value(value):
    if value is None:
        return ''
    return value


def get_value(tuple, key):
    if key not in tuple:
        return ''
    return check_value(tuple[key])


def check_int(value):
    if value is None:
        return 0
    return value


def get_int(tuple, key):
    if key not in tuple:
        return 0
    return int(check_value(tuple[key]))


def add_params(root, params):
    return '%s?%s' % (root, urllib.parse.urlencode(params))



def get_params(text):
    param = []
    paramstring = text
    if (len(paramstring) >= 2):
        params = text
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if len(splitparams) == 2:
                param[splitparams[0]] = urllib.parse.unquote_plus(splitparams[1])
    return param
