RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
while [ 1 ]; do
    echo ""
    echo "	1- Exécution des scripts tests"
    echo "	2- Exécution du code main (à éxecuter une fois pour chaque molécule)"
    echo "	404- Exit"
    echo ""
    read -p "	Veuillez taper votre choix ici s'ils vous plaît: " variable 


    if [ $variable = 1 ]; then
        echo ""
        echo "			    ${RED}Exécution du code test benzène ${NC}"
        echo ""
        python3 test_benzen.py


        echo ""
        echo "			       ${RED}Exécution du code test H2O ${NC}"
        echo ""
        python3 test_h2o.py


        echo ""
        echo "			${RED}Exécution du code test complexite temps ${NC}"
        echo ""
        python3 test_complexite_temps.py

    elif [ $variable = 2 ]; then
        echo ""
        echo "			        ${RED}Exécution du code main ${NC}"
        echo ""
        python3 Main.py

    elif [ $variable = 404 ]; then
        echo ""
        echo "			Merci pour votre visite"
        echo ""
        break
    fi



done
