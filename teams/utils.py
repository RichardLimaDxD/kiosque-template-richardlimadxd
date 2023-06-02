from datetime import datetime
from teams.exceptions import NegativeTitlesError
from teams.exceptions import InvalidYearCupError
from teams.exceptions import ImpossibleTitlesError


def data_processing(data):
    message_negative = "titles cannot be negative"

    message_invalid = "there was no world cup this year"

    message_impossible = "impossible to have more titles than disputed cups"

    if data["titles"] < 0:
        raise NegativeTitlesError(message_negative)

    create_data = int(datetime.now().year)

    get_years = [year for year in range(1930, create_data, 4)]

    get_cup = data["first_cup"]

    model_data = f"%Y-%m-%d"

    formated_firts_data = datetime.strptime(get_cup, model_data)

    convert_data = int(formated_firts_data.strftime("%Y"))

    if convert_data not in get_years:
        raise InvalidYearCupError(message_invalid)

    get_index_year = get_years.index(get_years[-1])

    get_index_date = get_years.index(convert_data)

    first_cup = get_index_year - get_index_date

    if data["titles"] > first_cup:
        raise ImpossibleTitlesError(message_impossible)
