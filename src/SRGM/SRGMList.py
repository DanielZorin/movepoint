'''
Created on 06.04.2011

@author: juan
'''
from .SRGM import SRGM
from .GoelOkumoto import GoelOkumoto
from .JelinskiMoranda import JelinskiMoranda
from .LittlewoodVerrall import LittlewoodVerrall
from .SShaped import SShaped
from .Logarithmic import Logarithmic

SRGMList = {"Goel-Okumoto":GoelOkumoto,
            "Jelinski-Moranda":JelinskiMoranda,
            "S-Shaped":SShaped,
            "Logarithmic":Logarithmic,
            "Littlewood-Verrall":LittlewoodVerrall}