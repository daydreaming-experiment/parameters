Daydreaming parameters
======================

This repository contains the various versions of parameters used in the [daydreaming experiment](http://daydreaming-the-app.net/). These parameters include question details, probe scheduling settings, and probably more things in the future. The app itself directly retrieves the parameters from this repository when it needs to; there is no other mirror.

File orgnisation
----------------

There are three important axes organising these files:

**Grammar version:** there is a kind of grammar to express the parameters, and this grammar will evolve as we add more features and integrate requirements into the app. All the versions of the grammar are described in `GRAMMAR.md`. Files for grammar version `X` are in folder `grammar-vX`.

**Testing or production mode:** there are three types of actors involved in this experiment: developers writing code (and this documentation), researchers tweaking parameters, and subjects participating in the experiment. When used by the subjects, the app normally fetches the *production* parameters. But when researchers want to tweak those parameters with trial and error, they enter the *testing mode* in the app: the app will then look for the *testing* parameters, which the researchers can modify without breaking the *production* configuration used by subjects participating in the experiment at the same time. Once the researchers are satisfied with the new parameters, they can replace the *production* version of the parameters file, and newly arriving subjects will be using those new parameters.

The *production* parameters file for grammar version `X` is `grammar-vX/production.json`. The corresponding *testing* parameters file is `grammar-vX/test.json`. Later on we could maybe add a *quality assessment* level.

**Development mode:** so that developers can test and play around with all this, they need a version of all these files for themselves. Their development version of the app fetches files like `dev/grammar-vX/production.json` and `dev/grammar-vX/test.json`.
