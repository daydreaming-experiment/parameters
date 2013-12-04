Daydreaming parameters
======================

This repository contains the various versions of parameters used in the [daydreaming experiment](http://daydreaming-the-app.net/). These parameters include question details, probe scheduling settings, and probably more things in the future. The app itself directly retrieves the parameters from this repository when it needs to; there is no other mirror.

File orgnisation
----------------

There are three important axes organising these files:

**Grammar version:** there is a kind of grammar to express the parameters, and this grammar will evolve as we add more features and integrate requirements into the app. Files for grammar version `X` are in folder `grammar-vX`, and each grammar version is extensively described in `grammar-vX/GRAMMAR.md` (version names follow [Semantic Versioning](http://semver.org/)). The grammar versions used in each version of the app are recorded in [`GRAMMAR-VERSIONS.md`](https://github.com/daydreaming-experiment/app/blob/master/GRAMMAR-VERSIONS.md) in the [daydreaming app](https://github.com/daydreaming-experiment/app/) repository.

**Testing or production mode:** there are three types of actors involved in this experiment: developers writing code (and this documentation), researchers tweaking parameters, and subjects participating in the experiment. When used by the subjects, the app normally fetches the *production* parameters. But when researchers want to tweak those parameters with trial and error, they enter the *testing mode* in the app: the app will then look for the *testing* parameters, which the researchers can modify without breaking the *production* configuration used by subjects participating in the experiment at the same time. Once the researchers are satisfied with the new parameters, they can replace the *production* version of the parameters file, and newly arriving subjects will be using those new parameters.

The *production* parameters file for grammar version `X` is `grammar-vX/production.json`. The corresponding *testing* parameters file is `grammar-vX/test.json`. Later on we could maybe add a *quality assessment* level.

**Development mode:** so that developers can test and play around with all this, they need a version of all these files for themselves. Their development version of the app fetches files like `dev/grammar-vX/production.json` and `dev/grammar-vX/test.json`.

Parameters update instructions
------------------------------

Follow these steps to update parameters for the app:

1. Check the grammar version used in the latest version of the app: head over to [`GRAMMAR-VERSIONS.md`](https://github.com/daydreaming-experiment/app/blob/master/GRAMMAR-VERSIONS.md) in the [daydreaming app](https://github.com/daydreaming-experiment/app/) repository. Then read carefully `grammar-vX/GRAMMAR.md`.
2. Since you don't know what the last tester did with the corresponding `grammar-vX/test.json` file (in *this* repository), start from scratch by copying `grammar-vX/production.json` to `grammar-vX/test.json` (unless you can read git commit logs and you know you were the last person to edit the test file); this will either overwrite the existing test file or create a new one if it doesn't already exist. You can do all this either directly on GitHub's website, or with your own clone of the repository.
3. Edit `grammar-vX/test.json`, and commit your changes (again, either on the GitHub website or by commiting on your clone and pushing to GitHub).
4. If you can, validate your test file by using the provided `grammar-vX/validate.py` script: if you are at the root of the repository, you can do this on a Linux distribution by running `python grammar-vX/validate.py grammar-vX/test.json` (where you replace `vX` with the real grammar version; you'll also need `python` installed).
5. Enter *testing mode* in the app on your phone (from the options screen). Then use the new buttons on the app dashboard to reset your test profile; you'll be presented with a new *test* first-launch sequence, during which the app will update its test parameters to the ones you just committed.
6. Play around with the app in test mode to try those new parameters.
7. Repeat steps 3-6 until you're happy.
8. Put your new parameters into production: copy `grammar-vX/test.json` to `grammar-vX/production.json`, replace the contents of `grammar-vX/test.json` with a single comment line (so that no one is misguided into using your draft test file in later tests), and commit.

That's it!
