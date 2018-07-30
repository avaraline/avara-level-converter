from Converter import resource
from Converter.converter import Converter
import Converter.pict.reader as pReader
import Converter.bspt.reader as bsptReader
import Converter.tmpl.reader as tmplReader
from lxml import etree
import argparse
import sys
import json

try:
    import audioop
except:
    print("python module `audioop` not found, no sounds will be exported")


def try_read(file):
    f = open(file, 'rb')
    data = f.read()

    if len(data) == 0:
        print("Couldn't read resource fork directly")

        f = open(file + '/..namedfork/rsrc', 'rb')
        data = f.read()

        if len(data) == 0:
            print("Couldn't read resource fork from /..namedfork/")
            return False
        else:
            return data
    else:
        return data


def get_resources(file):
    data = try_read(file)
    if data is False:
        print("No data to read")
        sys.exit(1)
    reader = resource.Reader()
    resources = reader.parse(data)

    return resources


def save_shapes(resource):
    bsps = bsptReader.parse(resource)
    for bsp in bsps:
        filename = "%d_%s.avarabsp.json" % (bsp.res_id, bsp.name)
        print("Writing BSPT %s" % filename)
        with open(filename, "w") as bsp_file:
            json.dump(
                bsp.serialize(),
                bsp_file,
                separators=(',', ': '))


def save_maps(resource, set_ledi):
    for pict in resource.values():
        pictname = pict['name']
        # pict name search, case insensitive
        # "*****" is the key for the list of levels in a set
        # don't ask me why, its a resedit thing
        ledi = [x for x in set_ledi['*****'] if x['Path'].lower() == pictname.lower()]
        if len(ledi) < 1:
            print("No LEDI found for '%s', skipping" % pictname)
            continue
        else:
            ledi = ledi[0]

        ops = pReader.parse(pict['data'])
        conv = Converter()
        mapxml = conv.convert(ops)


        filename = ledi['Tag'] + "_" + pictname + '.xml'
        print("Writing level %s to %s" % (ledi['Name'], filename))

        if mapxml is None:
            print("Error converting " + filename)
            continue

        xmlstring = etree.tostring(mapxml, pretty_print=True)
        with open(filename, 'w') as f:
            f.write(xmlstring.decode('macintosh'))


def convert_set(resources):
    # if 'HSND' in resources:
    #    save_hsnds(resources['HSND'])
    if 'BSPT' in resources:
        save_shapes(resources['BSPT'])
    tmplData = tmplReader.parse(resources)

    set_ledi = tmplData['LEDI'][128]
    set_name = set_ledi['Set Tag']

    save_maps(resources['PICT'], set_ledi)

    # export all TEXT as json
    if 'TEXT' in resources:
        result = {}
        texts = resources["TEXT"]
        for key in texts.keys():
            text = texts[key]
            result[key] = {
                'name' : text["name"],
                'text' : text["data"].decode('macintosh')
            }

        text_name = set_name + ".text"
        with open(text_name, "w") as text_file:
            json.dump(
                result,
                text_file)
        print("Exported TEXT to %s" % text_name)

    # export all LEDI as json (not really necessary)
    ledi_name = set_name + ".ledi"
    with open(ledi_name, "w") as ledi_file:
        json.dump(
            set_ledi,
            ledi_file,
            separators=(',', ': '))
    print("Exported LEDI to %s" % ledi_name)

    # export all HULL as json
    if 'HULL' in tmplData:
        hull_name = set_name + ".hull"
        with open(hull_name, "w") as hull_file:
            json.dump(
                tmplData['HULL'],
                hull_file,
                separators=(',', ': '))
        print("Exported HULL to %s" % hull_name)

    # BSPS holds shape scaling data, but it doesn't 
    # seem like it was really used
    
    # Avara itself has this resource, but there are
    # only three records and two of them don't even do 
    # anything

    # if 'BSPS' in tmplData:
    #    print(tmplData['BSPS'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', metavar='file')

    args = parser.parse_args()

    resources = get_resources(args.file)

    print("Found resources: %s" % ", ".join(resources.keys()))

    convert_set(resources)
