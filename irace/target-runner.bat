@echo off
::##############################################################################
:: BAT version of target-runner for Windows.
:: Contributed by Andre de Souza Andrade <andre.andrade@uniriotec.br>.
:: Check other examples in examples/
::
:: This script is run in the execution directory (execDir, --exec-dir).
::
:: PARAMETERS:
:: %%1 is the candidate configuration number
:: %%2 is the instance ID
:: %%3 is the seed
:: %%4 is the instance name
:: The rest are parameters to the target-algorithm
::
:: RETURN VALUE:
:: This script should print one numerical value: the cost that must be minimized.
:: Exit with 0 if no error, with 1 in case of error
::##############################################################################

:: Please change the EXE and FIXED_PARAMS to the correct ones
SET "exe=python"
SET "fixed_params=irace_test.py"

FOR /f "tokens=1-4*" %%a IN ("%*") DO (
	SET candidate=%%a
	SET instance_id=%%b
	SET seed=%%c
	SET instance=%%d
	SET candidate_parameters=%%e
)

SET "stdout=c%candidate%-%instance_id%-%seed%.stdout"
SET "stderr=c%candidate%-%instance_id%-%seed%.stderr"

:: :: FIXME: How to implement this in BAT ?
::if not exist %exe% error "%exe%: not found or not executable (pwd: %(pwd))"

:: Save  the output to a file, and parse the result from it.

%exe% %fixed_params% -i %instance% --seed %seed% %candidate_parameters% 1>%stdout% 2>%stderr%

:: read the resull from the stdout
set /p cost=<%stdout%
echo %cost%
:: return 0 if no error

:: clear the temporary files
del %stdout%
del %stderr%

exit 0
