Daydreaming parameters
======================

This repository contains the various versions of parameters used in the [daydreaming experiment](http://daydreaming-the-app.net/). These parameters include question details, probe scheduling settings, and probably more things in the future. The app itself directly retrieves the parameters from this repository when it needs to; there is no other mirror.

File orgnisation
----------------

There are three important axes organising these files:

**Grammar version:** there is a kind of grammar to express the parameters, and this grammar will evolve as we add more features and integrate requirements into the app. All the versions of the grammar are described in `GRAMMAR.md`. Files for grammar version `X` are in folder `grammar-vX`. The grammar used in each version of the app recorded in [`GRAMMAR-VERSIONS.md`](https://github.com/daydreaming-experiment/app/blob/master/GRAMMAR-VERSIONS.md) in the [daydreaming app](https://github.com/daydreaming-experiment/app/) repository.

**Testing or production mode:** there are three types of actors involved in this experiment: developers writing code (and this documentation), researchers tweaking parameters, and subjects participating in the experiment. When used by the subjects, the app normally fetches the *production* parameters. But when researchers want to tweak those parameters with trial and error, they enter the *testing mode* in the app: the app will then look for the *testing* parameters, which the researchers can modify without breaking the *production* configuration used by subjects participating in the experiment at the same time. Once the researchers are satisfied with the new parameters, they can replace the *production* version of the parameters file, and newly arriving subjects will be using those new parameters.

The *production* parameters file for grammar version `X` is `grammar-vX/production.json`. The corresponding *testing* parameters file is `grammar-vX/test.json`. Later on we could maybe add a *quality assessment* level.

**Development mode:** so that developers can test and play around with all this, they need a version of all these files for themselves. Their development version of the app fetches files like `dev/grammar-vX/production.json` and `dev/grammar-vX/test.json`.

Parameters update instructions
------------------------------

Follow these steps to update parameters for the app:

1. Check the grammar version used in the latest version of the app: head over to [`GRAMMAR-VERSIONS.md`](https://github.com/daydreaming-experiment/app/blob/master/GRAMMAR-VERSIONS.md) in the [daydreaming app](https://github.com/daydreaming-experiment/app/) repository.
2. Edit the corresponding `grammar-vX/test.json` file in *this* repository. You can do this either directly on GitHub's website, or with your own copy of the repository.
3. Commit your changes (again, either on the GitHub website or by commiting on your copy and pushing to GitHub)
4. Enter *testing mode* in the app on your phone. Then, use the new buttons on the app dashboard to either update the test app parameters or reset your test profile (which will also update the test app parameters).
5. Play around with the app to test those new parameters
6. Repeat steps 2-5 until you're happy
7. Put your new parameters into production: copy `grammar-vX/test.json` to `grammar-vX/production.json` and commit.

That's it!
