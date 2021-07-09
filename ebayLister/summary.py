def summaryPrintOut(errors, warnings):
    print('***********************************************')
    print('-------------SUMMARY OF OPERATIONS-------------')
    print('There are ' + str(len(errors)) + ' errors')
    print('There are ' + str(len(warnings)) + ' warnings')
    print('***********************************************')
    print('-------------WARNINGS-------------')
    for warning in warnings:
        print(warning)