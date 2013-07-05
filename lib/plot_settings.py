import ast
import ConfigParser
from drawing import RGB
import sys
import pandas

def default_hive_settings():

    """ Creates dictionary containing the default hive plot settings

    """

    hive_settings = {}

    hive_settings['dimension'] = 1000
    hive_settings['output_file_path']='hive.svg'
    hive_settings['draw_hive_plot'] = True

    hive_settings['tick_marks'] = True
    hive_settings['axis_subdivision'] = 0.05
    hive_settings['tick_labels'] = True
    hive_settings['tick_label_font_size'] = 0
    hive_settings['tick_label_distance'] = 3
    hive_settings['tick_height'] = 3
    hive_settings['tick_thickness'] = 1
    
    hive_settings['axis_start_radius'] = 50
    hive_settings['axis_end_radius'] = 600
    hive_settings['axis_thickness'] = 40
    hive_settings['axis_angles'] = [0]
    hive_settings['custom_scale'] = []

    hive_settings['draw_bars'] = True
    
    hive_settings['axis_colors'] = [0,0,0]
    hive_settings['bezier_colors'] = [[255,0,0],[0,255,0],[0,0,255]]

    hive_settings['use_custom_axis_labels'] = False
    hive_settings['axis_labels'] = None
    hive_settings['bezier_thickness'] = 10

    hive_settings['include_key'] = True
    hive_settings['key_position'] = ['-700','-700']
    hive_settings['key_font_size'] = 10
    hive_settings['key_title'] = 'Key'
    hive_settings['key_text_color'] = [0,0,0]
    hive_settings['key_title_size'] = 15

    return hive_settings



def default_struct_settings():

    ''' Creates dictionary containing the default structure plot settings

    '''

    struct_settings = {}
    struct_settings['draw_struct_plot'] = True
    struct_settings['output_file_path']='structure.svg'

    struct_settings['plot_width']=1000
    struct_settings['plot_height']=600

    struct_settings['left_margin']=100
    struct_settings['right_margin']=100
    struct_settings['top_margin']=100
    struct_settings['bottom_margin']=100

    struct_settings['colors']=[[200,10,10],[10,200,10],[10,10,200]]
    struct_settings['axis_color']=[0,0,0]

    struct_settings['axis_thickness']=2

    struct_settings['tick_length']=10

    struct_settings['horiz_label_size']=15
    struct_settings['horiz_label_spacing']=20

    struct_settings['horiz_axis_title']='title'
    struct_settings['horiz_axis_title_size']=30
    
    struct_settings['use_vertical_ticks']=True
    struct_settings['vertical_tick_spacing']=0.2
    struct_settings['vert_label_size']=15
    struct_settings['vert_label_spacing']=20


    struct_settings['include_key'] = False
    struct_settings['key_title'] = 'Title'
    struct_settings['key_title_size'] = 10
    struct_settings['key_position'] = [800,200]
    struct_settings['key_labels'] = None
    struct_settings['key_font_size'] = 15
    struct_settings['key_text_color'] = [0,0,0]
    struct_settings['use_custom_key_labels']=False

    return struct_settings

def default_sashimi_settings():
    sashimi_settings = {}

    sashimi_settings['width'] = 7
    sashimi_settings['height'] = 5

    sashimi_settings['intron_scale'] = 1
    sashimi_settings['exon_scale'] = 1
    sashimi_settings['colors'] = [[200,10,10],[10,200,10],[10,10,200]] 
    sashimi_settings['ymax'] = None
    sashimi_settings['number_junctions'] = True
    sashimi_settings['resolution'] = 0.5
    sashimi_settings['junction_log_base'] = 10
    sashimi_settings['reverse_minus'] = False
    sashimi_settings['font_size'] = 6
    sashimi_settings['nyticks'] = 3
    sashimi_settings['nxticks'] = 4
    sashimi_settings['show_ylabel'] = True
    sashimi_settings['show_xlabel'] = True

    return sashimi_settings


def parse_hive_plot_settings(config,data):

    ''' Parses custom settings for a hive plot from a configuration file. Returns a dictionary containing all
    of the settings

    config is a ConfigParser object which already contains all of the settings
    data is a pandas.DataFrame object containing all of the alternative splicing data

    '''
    print 'Parsing settings for hive plot...'

    settings = default_hive_settings()
    
    INTEGER_PARAMS = {'dimension'}
    FLOAT_PARAMS = {'axis_subdivision',
                        'tick_label_font_size',
                        'tick_label_distance',
                        'axis_start_radius',
                        'axis_end_radius',
                        'bezier_thickness',
                        'axis_thickness',
                        'tick_height',
                        'tick_thickness',
                        'axis_label_size',
                        'key_font_size',
                        'key_title_size'}
    BOOLEAN_PARAMS = {'tick_marks',
                        'tick_labels',
                        'draw_bars',
                        'use_custom_axis_labels',
                        'include_key',
                        'draw_hive_plot'}
    OTHER_PARAMS = {'axis_colors',
                        'bezier_colors',
                        'axis_angles',
                        'data',
                        'custom_scale',
                        'axis_labels',
                        'axis_label_radius',
                        'key_position',
                        'key_title',
                        'key_text_color',
                        'key_position',
			'output_file_path'}
    for option in config.options('hive_plot'):
        if option in INTEGER_PARAMS:
            settings[option] = config.getint('hive_plot',option)
        elif option in FLOAT_PARAMS:
            settings[option] = config.getfloat('hive_plot',option)
        elif option in BOOLEAN_PARAMS:
            settings[option] = config.getboolean('hive_plot',option)
        elif option in OTHER_PARAMS:
            settings[option] = ast.literal_eval(config.get('hive_plot',option))

    # check to make sure that the settings have the right format and preprocess them
    number_of_junctions = len(data.columns[1:])
    number_of_genotypes = len(set(data.icol(0)))

    if 'axis_angles' not in settings:
        axis_angles = map(lambda x: 360 / number_of_junctions, list(range(number_of_junctions)))
        settings['axis_angles'] = axis_angles
    elif type(settings['axis_angles']) is not list or len(settings['axis_angles']) != number_of_junctions:
        print 'Invalid number of elements in axis_angles'
        sys.exit(1)

    if len(settings['bezier_colors']) < number_of_genotypes:
        print 'Invalid number of elements in bezier_colors'
        sys.exit(1)
    else:
        colorified = [None] * len(settings['bezier_colors'])
        try:
            for i in range(len(colorified)):
                colorified[i] = RGB.from_list(settings['bezier_colors'][i])
            settings['bezier_colors'] = colorified
        except Exception:
            print 'Invalid colors in bezier_colors'
            sys.exit(1)

    try:
        settings['axis_colors'] = RGB.from_list(settings['axis_colors'])
    except Exception:
        print 'Invalid color in axis_colors'
        sys.exit(1)

    if settings['custom_scale']:
        if type(settings['custom_scale']) is not list:
            print 'custom_scale must be list'
            sys.exit(1)
        if len(settings['custom_scale']) < number_of_genotypes:
            print 'Invalid number of elements in custom_scale'
            sys.exit(1)
        for item in settings['custom_scale']:
            if type(item) is not list:
                print 'Items in custom_scale must be list'
                sys.exit(1)
            elif len(item) != 2:
                print 'Invalid number of elements in element of custom_scale'
                sys.exit(1)
            elif item[0] < 0 or item[0] > 1 or item[1] < item[0] or item[1] > 1:
                print 'Invalid boundary in custom_scale'
                sys.exit(1)

    if settings['use_custom_axis_labels']:
        if type(settings['axis_labels']) is not list:
            print 'axis_labels must be a list'
            sys.exit(1)
        if type(settings['axis_label_radius']) is not list:
            print 'axis_label_radius must be a list'
            sys.exit(1)
        if len(settings['axis_labels']) != number_of_junctions:
            print 'Invalid number of axis_labels'
            sys.exit(1)
        if len(settings['axis_label_radius']) != number_of_junctions:
            print 'Invalid number of elements in axis_label_radius'
            sys.exit(1)

    if settings['include_key']:
        if type(settings['key_title']) is not str:
            print 'key_title must be string'
            sys.exit(1)
        if type(settings['key_position']) is not list:
            print 'key_position must be list'
            sys.exit(1)
        if type(settings['key_text_color']) is not list:
            print 'key_text_color must be list'
            sys.exit(1)

        if len(settings['key_position']) != 2:
            print 'key_position can have exactly 2 coordinates'
            sys.exit(1)

        if len(settings['key_text_color']) != 3:
            print 'key_text_color must have exactly 3 components'
            sys.exit(1)

        for color in settings['key_text_color']:
            if color < 0 or color > 255:
                print 'components of key_text_color must be between 0 and 255'
                sys.exit(1)

        settings['key_text_color'] = RGB.from_list(settings['key_text_color'])
    
    return settings

def parse_struct_plot_settings(config_parser,data):
    ''' Parses custom settings for a structure plot from a configuration file. Returns a dictionary containing
    all of the settings

    config is a ConfigParser object which already contains all of the settings
    data is a pandas.DataFrame object containing all of the alternative splicing data

    '''
    print 'Parsing settings for structure plot...'
    
    settings = default_struct_settings()

    INTEGER_PARAMS = {'plot_width',
                        'plot_height',
                        'left_margin',
                        'right_margin',
                        'top_margin',
                        'bottom_margin'}
    FLOAT_PARAMS = {'axis_thickness',
                        'tick_length',
                        'horiz_label_size',
                        'horiz_label_spacing',
                        'horiz_axis_title_size',
                        'horiz_axis_title_spacing',
                        'vertical_tick_spacing',
                        'vert_label_size',
                        'vert_label_spacing',
                        'key_title_size',
                        'key_font_size'}
    BOOLEAN_PARAMS = {'draw_struct_plot',
                        'use_vertical_ticks',
                        'include_key',
                        'use_custom_key_labels'}
    OTHER_PARAMS = {'horiz_axis_title',
                        'colors',
                        'axis_color',
                        'output_file_path',
                        'key_title',
                        'key_labels',
                        'key_text_color',
                        'key_position'}


    for option in config_parser.options('struct_plot'):
        if option in INTEGER_PARAMS:
            settings[option] = config_parser.getint('struct_plot',option)
        elif option in FLOAT_PARAMS:
            settings[option] = config_parser.getfloat('struct_plot',option)
        elif option in BOOLEAN_PARAMS:
            settings[option] = config_parser.getboolean('struct_plot',option)
        elif option in OTHER_PARAMS:
            settings[option] = ast.literal_eval(config_parser.get('struct_plot',option))


    # check to make sure entries in settings have the correct format
    

    if type(settings['colors']) is not list:
        print 'colors must be a list of 3 element lists'
        sys.exit(1)
    if len(settings['colors']) < data.shape[1] - 1:
        print 'there are not enough colors in colors'
        sys.exit(1)
    else:
        colorified = [None] * len(settings['colors'])
        try:
            for i in range(len(colorified)):
                colorified[i] = RGB.from_list(settings['colors'][i])
            settings['colors'] = colorified
        except Exception:
            print 'Invalid colors in colors'
            sys.exit(1)

    try:
        settings['axis_color'] = RGB.from_list(settings['axis_color'])
    except Exception:
        print 'Invalid color in axis_color'
        sys.exit(1)

    if settings['include_key']:
        try:
            settings['key_text_color'] = RGB.from_list(settings['key_text_color'])
        except Exception:
            print 'Invalid color in key_text_color'
            sys.exit(1)

        if settings['key_labels'] == None:
            settings['key_labels'] = data.columns[1:]
        elif len(settings['key_labels']) != len(data.columns[1:]):
            print 'Incorrect number of labels for key'
            sys.exit(1)

        if len(settings['key_position']) != 2:
            print 'Invalid number of components in key_position'
            sys.exit(1)

        for i in range(2):
            try:
                settings['key_position'][i] = int(settings['key_position'][i])
            except Exception:
                print 'Elements in key_position must be numbers'
                sys.exit(1)

    return settings


def parse_sashimi_settings(config_parser):
    settings = default_sashimi_settings()

    FLOAT_PARAMS = {'width',
                    'height',
                    'intron_scale',
                    'exon_scale',
                    'ymax',
                    'resolution',
                    'junction_log_base',
                    'font_size'}

    INT_PARAMS = {'nyticks',
                    'nxticks'}

    BOOLEAN_PARAMS = {'number_junctions',
                    'reverse_minus',
                    'show_ylabel',
                    'show_xlabel'}

    OTHER_PARAMS = {'colors'}


    for option in config_parser.options('sashimi_plot'):
        if option in INTEGER_PARAMS:
            settings[option] = config_parser.getint('struct_plot',option)
        elif option in FLOAT_PARAMS:
            settings[option] = config_parser.getfloat('struct_plot',option)
        elif option in BOOLEAN_PARAMS:
            settings[option] = config_parser.getboolean('struct_plot',option)
        elif option in OTHER_PARAMS:
            settings[option] = ast.literal_eval(config_parser.get('struct_plot',option))

    # make sure that parameters are valid

    
    return settings



def parse_settings(settings_file):

    """ Creates multiple dictionaries containing the settings parsed from a settings file.
    Each type of plot has its own settings dictionary.
    
    settings_file is the name of the text file containing the settings

    Return values:
    data is a pandas.DataFrame object which contains the alternative splicing data
    hive_plot_settings is a dictionary containing the settings for the hive plot
    struct_plot_settings is a dictionary containing the settings for the structure plot
    """

    config = ConfigParser.ConfigParser()
    print 'Reading settings from {0}...'.format(settings_file)
    config.read(settings_file)

    data = create_data_frame_from_file(ast.literal_eval(config.get('data','data')))

    hive_plot_settings = parse_hive_plot_settings(config,data)
    struct_plot_settings = parse_struct_plot_settings(config,data)


    print 'Done reading settings.'
    return data, hive_plot_settings, struct_plot_settings




def create_data_frame_from_file(file_name):

    """ Creates a pandas.DataFrame object containing splicing expression information by reading a text file.

    file_name is the name of the file containing the splicing expression
    """

    try:
        f1 = open(file_name,'r').readlines()
        header = f1[0].strip('\n').split('\t')

        col_names = header[1:]

        construction_data_dict = {}
        
        for i in range(1,len(f1)):
            line = f1[i].strip('\n').split('\t')

            expression_values = map(float,line[2:])
            line[2:] = expression_values

            indiv_name = line[0]
            construction_data_dict[indiv_name] = pandas.Series(line[1:],col_names)

        data_frame = pandas.DataFrame(construction_data_dict).T
        return data_frame
            

    except IOError:
        print 'Invalid data file'
        sys.exit(1)