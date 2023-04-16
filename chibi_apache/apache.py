# -*- coding: utf-8 -*-
from chibi.atlas.multi import Chibi_atlas_multi


def parse( content ):
    content = filter( bool, content.split( '\n' ) )
    content = map( str.strip, content )
    content = filter( lambda x: not x.startswith( '#' ), content )
    result = parse_internal( content )
    return result


def to_string( d, tabs=0 ):
    result = "\n".join( iter_to_string( d, tabs=tabs ) )
    return result + '\n'


def iter_to_string( d, tabs=0 ):
    t = '    ' * tabs
    for k, v in d.items():
        if isinstance( v, dict ):
            for key, inner in v.items():
                yield ""
                yield f'{t}<{k} {key}>'
                yield from iter_to_string( inner, tabs=tabs + 1 )
                yield f'{t}</{k}>'
        elif isinstance( v, list ):
            for value in v:
                yield f'{t}{k} {value}'
            """
            for vv in v:
                if isinstance( vv, dict ):
                    yield f'{t}{k}' + ' {'
                    yield from iter_to_string( vv, tabs + 1 )
                    yield f'{t}' + '}'
                else:
                    yield f'{t}{k} {vv};'
            """
        else:
            yield f'{t}{k} {v}'


def parse_internal( content_iter ):
    result = Chibi_atlas_multi()
    for line in content_iter:
        if line.startswith( '</' ):
            return result
        elif line.startswith( '<' ):
            line = line.replace( '<', '' ).replace( '>', '' )
            key, value = line.split( ' ', 1 )
            if key not in result:
                result[ key ] = Chibi_atlas_multi()
            result[ key ][ value ] = parse_internal( content_iter )
        else:
            key, value = line.split( ' ', 1 )
            result[ key ] = value
    return result
