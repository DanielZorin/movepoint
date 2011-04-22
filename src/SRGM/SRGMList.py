'''
Created on 06.04.2011

@author: juan
'''

from SRGM.GoelOkumoto import GoelOkumoto
from SRGM.JelinskiMoranda import JelinskiMoranda
from SRGM.LittlewoodVerrall import LittlewoodVerrall
from SRGM.SShaped import SShaped
from SRGM.Logarithmic import Logarithmic

SRGMList = {"Goel-Okumoto":GoelOkumoto,
            "Jelinski-Moranda":JelinskiMoranda,
            "S-Shaped":SShaped,
            "Logarithmic":Logarithmic,
            "Littlewood-Verrall":LittlewoodVerrall}