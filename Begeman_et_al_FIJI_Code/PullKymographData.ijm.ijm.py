#@ File (label="Select a save directory", style="directory") savedir
from ij.gui import Roi
from ij import IJ, WindowManager, ImagePlus
from ij.gui import ProfilePlot
from ij.measure import ResultsTable
from ij.plugin.frame import RoiManager
import os, glob, sys

RM = RoiManager()
roi_manager = RM.getRoiManager()
roi_manager.select(1)
table = ResultsTable()
image = IJ.getImage()
for i in range(0, image.getStack().getSize()):
	image.setSlice(i + 1)
	profile = ProfilePlot(image)
	profile = profile.getProfile()
	table.setValues('time point' + str(i), profile)

table.save(savedir.getPath() + '/' + image.getShortTitle() + '_nonbleach.csv')
