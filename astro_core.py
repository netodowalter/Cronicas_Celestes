from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone as dt_timezone
from typing import Any, Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

import swisseph as swe


swe.set_ephe_path(None)


PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "North Node": swe.MEAN_NODE,
}

MAIN_PLANETS = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
POINTS_FOR_OUTPUT = MAIN_PLANETS + ["North Node", "South Node", "Part of Fortune"]

ZODIAC = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

ZODIAC_PT = {
    "Aries": "Áries",
    "Taurus": "Touro",
    "Gemini": "Gêmeos",
    "Cancer": "Câncer",
    "Leo": "Leão",
    "Virgo": "Virgem",
    "Libra": "Libra",
    "Scorpio": "Escorpião",
    "Sagittarius": "Sagitário",
    "Capricorn": "Capricórnio",
    "Aquarius": "Aquário",
    "Pisces": "Peixes",
}

ZODIAC_SYMBOLS = {
    "Aries": "♈",
    "Taurus": "♉",
    "Gemini": "♊",
    "Cancer": "♋",
    "Leo": "♌",
    "Virgo": "♍",
    "Libra": "♎",
    "Scorpio": "♏",
    "Sagittarius": "♐",
    "Capricorn": "♑",
    "Aquarius": "♒",
    "Pisces": "♓",
}

PLANET_SYMBOLS = {
    "Sun": "☉",
    "Moon": "☽",
    "Mercury": "☿",
    "Venus": "♀",
    "Mars": "♂",
    "Jupiter": "♃",
    "Saturn": "♄",
    "North Node": "☊",
    "South Node": "☋",
    "Part of Fortune": "⊗",
}

PLANET_PT = {
    "Sun": "Sol",
    "Moon": "Lua",
    "Mercury": "Mercúrio",
    "Venus": "Vênus",
    "Mars": "Marte",
    "Jupiter": "Júpiter",
    "Saturn": "Saturno",
    "North Node": "Nodo Norte",
    "South Node": "Nodo Sul",
    "Part of Fortune": "Parte da Fortuna",
}

SIGN_RULERS = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}

EXALTATIONS = {
    "Sun": ("Aries", 19),
    "Moon": ("Taurus", 3),
    "Mercury": ("Virgo", 15),
    "Venus": ("Pisces", 27),
    "Mars": ("Capricorn", 28),
    "Jupiter": ("Cancer", 15),
    "Saturn": ("Libra", 21),
    "North Node": ("Gemini", 3),
}

DETRIMENT = {
    "Sun": ["Aquarius"],
    "Moon": ["Capricorn"],
    "Mercury": ["Sagittarius", "Pisces"],
    "Venus": ["Aries", "Scorpio"],
    "Mars": ["Taurus", "Libra"],
    "Jupiter": ["Gemini", "Virgo"],
    "Saturn": ["Cancer", "Leo"],
}

FALL = {
    "Sun": "Libra",
    "Moon": "Scorpio",
    "Mercury": "Pisces",
    "Venus": "Virgo",
    "Mars": "Cancer",
    "Jupiter": "Capricorn",
    "Saturn": "Aries",
}

TRIPLICITY_RULERS = {
    "Fire": {"day": "Sun", "night": "Jupiter", "participating": "Saturn"},
    "Earth": {"day": "Venus", "night": "Moon", "participating": "Mars"},
    "Air": {"day": "Saturn", "night": "Mercury", "participating": "Jupiter"},
    "Water": {"day": "Venus", "night": "Mars", "participating": "Moon"},
}

TERMS = {
    "Aries": [("Jupiter", 6), ("Venus", 8), ("Mercury", 7), ("Mars", 7), ("Saturn", 2)],
    "Taurus": [("Venus", 8), ("Mercury", 7), ("Jupiter", 7), ("Saturn", 4), ("Mars", 4)],
    "Gemini": [("Mercury", 7), ("Jupiter", 6), ("Venus", 7), ("Saturn", 5), ("Mars", 5)],
    "Cancer": [("Mars", 6), ("Jupiter", 7), ("Mercury", 7), ("Venus", 7), ("Saturn", 3)],
    "Leo": [("Jupiter", 6), ("Venus", 5), ("Saturn", 7), ("Mercury", 6), ("Mars", 6)],
    "Virgo": [("Mercury", 7), ("Venus", 6), ("Jupiter", 5), ("Saturn", 6), ("Mars", 6)],
    "Libra": [("Saturn", 6), ("Mercury", 5), ("Jupiter", 8), ("Venus", 5), ("Mars", 6)],
    "Scorpio": [("Mars", 6), ("Jupiter", 6), ("Venus", 7), ("Mercury", 6), ("Saturn", 5)],
    "Sagittarius": [("Jupiter", 8), ("Venus", 6), ("Mercury", 5), ("Saturn", 6), ("Mars", 5)],
    "Capricorn": [("Mercury", 6), ("Jupiter", 6), ("Venus", 7), ("Saturn", 6), ("Mars", 5)],
    "Aquarius": [("Mercury", 7), ("Venus", 6), ("Jupiter", 7), ("Saturn", 5), ("Mars", 5)],
    "Pisces": [("Venus", 8), ("Jupiter", 6), ("Mercury", 6), ("Mars", 6), ("Saturn", 4)],
}

FACES = {
    "Aries": ["Mars", "Sun", "Venus"],
    "Taurus": ["Mercury", "Moon", "Saturn"],
    "Gemini": ["Jupiter", "Mars", "Sun"],
    "Cancer": ["Venus", "Mercury", "Moon"],
    "Leo": ["Saturn", "Jupiter", "Mars"],
    "Virgo": ["Sun", "Venus", "Mercury"],
    "Libra": ["Moon", "Saturn", "Jupiter"],
    "Scorpio": ["Mars", "Sun", "Venus"],
    "Sagittarius": ["Mercury", "Moon", "Saturn"],
    "Capricorn": ["Jupiter", "Mars", "Sun"],
    "Aquarius": ["Venus", "Mercury", "Moon"],
    "Pisces": ["Saturn", "Jupiter", "Mars"],
}

SIGN_ELEMENTS = {
    "Aries": "Fire",
    "Taurus": "Earth",
    "Gemini": "Air",
    "Cancer": "Water",
    "Leo": "Fire",
    "Virgo": "Earth",
    "Libra": "Air",
    "Scorpio": "Water",
    "Sagittarius": "Fire",
    "Capricorn": "Earth",
    "Aquarius": "Air",
    "Pisces": "Water",
}

DIURNAL_PLANETS = ["Sun", "Jupiter", "Saturn"]
NOCTURNAL_PLANETS = ["Moon", "Venus", "Mars"]
BENEFICS = ["Jupiter", "Venus"]
MALEFICS = ["Saturn", "Mars"]

AVERAGE_SPEEDS = {
    "Sun": 0.955,
    "Moon": 13.18,
    "Mercury": 1.38,
    "Venus": 1.2,
    "Mars": 0.68,
    "Jupiter": 0.13,
    "Saturn": 0.065,
}

HOUSE_SCORES = {
    1: ("Angular", 5),
    10: ("Angular", 5),
    7: ("Angular", 4),
    4: ("Angular", 4),
    11: ("Sucedente", 4),
    5: ("Sucedente", 3),
    2: ("Sucedente", 3),
    9: ("Cadente", 2),
    3: ("Cadente", 1),
    12: ("Cadente", -5),
    8: ("Cadente", -4),
    6: ("Cadente", -3),
}

VISUAL_ORBS = {
    "Sun": 12,
    "Moon": 10,
    "Mercury": 5,
    "Venus": 5,
    "Mars": 6,
    "Jupiter": 7,
    "Saturn": 7,
}

SIGN_ASPECT_ANGLES = {
    0: ("Conjunction", 0),
    2: ("Sextile", 60),
    3: ("Square", 90),
    4: ("Trine", 120),
    6: ("Opposition", 180),
}


@dataclass
class PlanetPosition:
    planet: str
    symbol: str
    longitude: float
    sign: str
    signIndex: int
    degree: int
    minute: int
    retrograde: bool
    speed: float
    house: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DignityResult:
    planet: str
    totalScore: int
    essentialScore: int
    accidentalScore: int
    essentialDetails: List[str]
    accidentalDetails: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AspectResult:
    planet1: str
    planet2: str
    aspect: str
    angle: int
    realDistance: float
    orb: float
    maxOrb: float
    phase: str
    bySign: bool
    moiety: float
    beneficStrength: int = 0
    maleficStrength: int = 0
    bonification: bool = False
    maltreatment: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_angle(angle: float) -> float:
    return angle % 360


def shortest_arc(angle_a: float, angle_b: float) -> float:
    diff = abs(normalize_angle(angle_a) - normalize_angle(angle_b))
    return 360 - diff if diff > 180 else diff


def zodiac_distance(from_lon: float, to_lon: float) -> float:
    return normalize_angle(to_lon - from_lon)


def get_sign_and_degree(longitude: float) -> Tuple[str, int, float]:
    longitude = normalize_angle(longitude)
    sign_index = int(longitude // 30)
    degree_in_sign = longitude % 30
    return ZODIAC[sign_index], sign_index, degree_in_sign


def decimal_to_degree_minute(value: float) -> Tuple[int, int]:
    degree = int(value)
    minute = int(round((value % 1) * 60))
    if minute == 60:
        degree += 1
        minute = 0
    return degree, minute


def local_datetime_to_utc(birth_date: str, birth_time: str, tz_name: str) -> datetime:
    local_dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
    aware_local = local_dt.replace(tzinfo=ZoneInfo(tz_name))
    return aware_local.astimezone(dt_timezone.utc)


def utc_datetime_to_julian_day(utc_dt: datetime) -> float:
    utc_hour = utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
    return swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_hour)


def get_planet_sect(planet: str) -> str:
    if planet in DIURNAL_PLANETS:
        return "day"
    if planet in NOCTURNAL_PLANETS:
        return "night"
    return "neutral"


def is_planet_in_sect(planet: str, is_day_chart: bool) -> bool:
    sect = get_planet_sect(planet)
    return (sect == "day" and is_day_chart) or (sect == "night" and not is_day_chart)


def whole_sign_house(sign_index: int, asc_sign_index: int) -> int:
    return ((sign_index - asc_sign_index + 12) % 12) + 1


def find_position(positions: List[PlanetPosition], planet: str) -> PlanetPosition:
    return next(p for p in positions if p.planet == planet)


def angular_distance(longitude_a: float, longitude_b: float) -> float:
    diff = abs(normalize_angle(longitude_a) - normalize_angle(longitude_b))
    return 360 - diff if diff > 180 else diff


def sign_distance(sign_index_a: int, sign_index_b: int) -> int:
    diff = abs(sign_index_a - sign_index_b) % 12
    return min(diff, 12 - diff)


def get_aspect_by_sign(sign_index_a: int, sign_index_b: int):
    diff = sign_distance(sign_index_a, sign_index_b)
    return SIGN_ASPECT_ANGLES.get(diff)


def calculate_moiety(planet_a: str, planet_b: str) -> float:
    orb_a = VISUAL_ORBS.get(planet_a, 0)
    orb_b = VISUAL_ORBS.get(planet_b, 0)
    return (orb_a + orb_b) / 2.0


def classify_aspect_phase(
    planet_a: str,
    longitude_a: float,
    planet_b: str,
    longitude_b: float,
    exact_angle: float,
) -> str:
    speed_a = AVERAGE_SPEEDS.get(planet_a, 0)
    speed_b = AVERAGE_SPEEDS.get(planet_b, 0)

    if speed_a == speed_b:
        d = angular_distance(longitude_a, longitude_b)
        return "applicative" if d > exact_angle else "separative"

    if speed_a > speed_b:
        faster_lon = longitude_a
        slower_lon = longitude_b
    else:
        faster_lon = longitude_b
        slower_lon = longitude_a

    rel = normalize_angle(faster_lon - slower_lon)
    if rel > exact_angle:
        return "applicative"
    return "separative"


def aspect_within_orb(
    real_distance: float,
    exact_angle: float,
    moiety: float,
    phase: str,
) -> tuple[bool, float, float]:
    orb = abs(real_distance - exact_angle)
    limit = moiety + 3 if phase == "applicative" else moiety + 1
    return orb <= limit, orb, limit


def build_planet_position(planet_name: str, longitude: float, speed: float) -> PlanetPosition:
    sign, sign_idx, degree_in_sign = get_sign_and_degree(longitude)
    degree, minute = decimal_to_degree_minute(degree_in_sign)
    return PlanetPosition(
        planet=planet_name,
        symbol=PLANET_SYMBOLS.get(planet_name, ""),
        longitude=normalize_angle(longitude),
        sign=sign,
        signIndex=sign_idx,
        degree=degree,
        minute=minute,
        retrograde=speed < 0,
        speed=speed,
    )


def build_south_node(north_node: PlanetPosition) -> PlanetPosition:
    south_lon = normalize_angle(north_node.longitude + 180)
    position = build_planet_position("South Node", south_lon, 0.0)
    position.retrograde = True
    return position


def build_part_of_fortune(asc_lon: float, sun_lon: float, moon_lon: float, is_day_chart: bool) -> PlanetPosition:
    if is_day_chart:
        pof_lon = normalize_angle(asc_lon + moon_lon - sun_lon)
    else:
        pof_lon = normalize_angle(asc_lon + sun_lon - moon_lon)

    position = build_planet_position("Part of Fortune", pof_lon, 0.0)
    position.retrograde = False
    return position


def is_diurnal_chart(asc_lon: float, sun_lon: float) -> bool:
    rel = zodiac_distance(asc_lon, sun_lon)
    return 180 <= rel < 360


def compute_essential_dignity(planet: str, sign: str, degree: float, is_day_chart: bool) -> Tuple[int, List[str]]:
    score = 0
    details: List[str] = []

    if SIGN_RULERS.get(sign) == planet:
        score += 5
        details.append(f"Domicílio em {ZODIAC_PT[sign]} +5")

    if planet in EXALTATIONS:
        exalt_sign, _ = EXALTATIONS[planet]
        if sign == exalt_sign:
            score += 4
            details.append(f"Exaltação em {ZODIAC_PT[sign]} +4")

    element = SIGN_ELEMENTS.get(sign)
    if element and element in TRIPLICITY_RULERS:
        sect_key = "day" if is_day_chart else "night"
        if TRIPLICITY_RULERS[element][sect_key] == planet:
            score += 3
            details.append(f"Triplicidade {'diurna' if is_day_chart else 'noturna'} de {ZODIAC_PT[sign]} +3")

    if sign in TERMS:
        term_deg = 0
        for term_planet, term_width in TERMS[sign]:
            if term_deg <= degree < term_deg + term_width:
                if term_planet == planet:
                    score += 2
                    details.append(f"Termo em {ZODIAC_PT[sign]} +2")
                break
            term_deg += term_width

    if sign in FACES:
        face_index = min(int(degree // 10), 2)
        if FACES[sign][face_index] == planet:
            score += 1
            details.append(f"Face/Decano em {ZODIAC_PT[sign]} +1")

    if planet in DETRIMENT and sign in DETRIMENT[planet]:
        score -= 5
        details.append(f"Exílio em {ZODIAC_PT[sign]} -5")

    if planet in FALL and FALL[planet] == sign:
        score -= 4
        details.append(f"Queda em {ZODIAC_PT[sign]} -4")

    has_positive_essential = any(
        text.startswith(("Domicílio", "Exaltação", "Triplicidade", "Termo", "Face"))
        for text in details
    )
    if not has_positive_essential and planet in MAIN_PLANETS:
        score -= 5
        details.append("Peregrino -5")

    return score, details


def compute_accidental_dignity(
    position: PlanetPosition,
    is_day_chart: bool,
    sun_lon: float,
) -> Tuple[int, List[str]]:
    score = 0
    details: List[str] = []

    house_type, house_value = HOUSE_SCORES.get(position.house or 0, ("Cadente", 0))
    if house_value != 0:
        score += house_value
        prefix = "+" if house_value > 0 else ""
        details.append(f"Casa {position.house} ({house_type}) {prefix}{house_value}")

    if position.retrograde:
        score -= 5
        details.append("Retrógrado -5")
    else:
        score += 4
        details.append("Direto +4")

    if position.planet in AVERAGE_SPEEDS:
        average_speed = AVERAGE_SPEEDS[position.planet]
        if abs(position.speed) > average_speed:
            score += 2
            details.append("Rápido +2")
        else:
            score -= 2
            details.append("Lento -2")

    if position.planet in DIURNAL_PLANETS:
        zodiac_dist = zodiac_distance(sun_lon, position.longitude)
        if 0 < zodiac_dist < 180:
            score += 2
            details.append("G/F/E oriental +2")
        else:
            score -= 2
            details.append("G/F/E ocidental -2")
    elif position.planet in NOCTURNAL_PLANETS or position.planet == "Mercury":
        zodiac_dist = zodiac_distance(sun_lon, position.longitude)
        if zodiac_dist > 180:
            score += 2
            details.append("D/C/B ocidental +2")
        else:
            score -= 2
            details.append("D/C/B oriental -2")

    if position.planet != "Sun":
        dist_from_sun = shortest_arc(position.longitude, sun_lon)
        if dist_from_sun < 0.5:
            score += 5
            details.append("Cazimi +5")
        elif dist_from_sun < 8:
            score -= 6
            details.append("Combusto -6")
        elif dist_from_sun < 17:
            score -= 4
            details.append("Sob os raios do Sol -4")
        else:
            score += 5
            details.append("Livre de combustão e raios +5")

    if position.planet == "Moon":
        moon_sun_dist = zodiac_distance(sun_lon, position.longitude)
        if moon_sun_dist < 180:
            score += 1
            details.append("Aumento de luz +1")
        else:
            score -= 1
            details.append("Diminuição de luz -1")

    if position.planet in DIURNAL_PLANETS:
        if is_day_chart:
            score += 0
        else:
            score += 0
    elif position.planet in NOCTURNAL_PLANETS:
        if not is_day_chart:
            score += 0
        else:
            score += 0

    return score, details


def calculate_dignities(
    positions: List[PlanetPosition],
    is_day_chart: bool,
    sun_lon: float,
) -> List[Dict[str, Any]]:
    results: List[DignityResult] = []

    for position in positions:
        if position.planet in ["North Node", "South Node"]:
            continue

        degree_decimal = position.degree + (position.minute / 60)
        essential_score, essential_details = compute_essential_dignity(
            planet=position.planet,
            sign=position.sign,
            degree=degree_decimal,
            is_day_chart=is_day_chart,
        )
        accidental_score, accidental_details = compute_accidental_dignity(
            position=position,
            is_day_chart=is_day_chart,
            sun_lon=sun_lon,
        )

        results.append(
            DignityResult(
                planet=position.planet,
                totalScore=essential_score + accidental_score,
                essentialScore=essential_score,
                accidentalScore=accidental_score,
                essentialDetails=essential_details,
                accidentalDetails=accidental_details,
            )
        )

    results.sort(key=lambda item: (item.essentialScore, item.accidentalScore, item.totalScore), reverse=True)
    return [item.to_dict() for item in results]


def calculate_aspects(positions: List[PlanetPosition], is_day_chart: bool) -> List[Dict[str, Any]]:
    aspects: List[AspectResult] = []

    planets_list = [p for p in positions if p.planet in MAIN_PLANETS]

    for i, p1 in enumerate(planets_list):
        for p2 in planets_list[i + 1 :]:
            by_sign_data = get_aspect_by_sign(p1.signIndex, p2.signIndex)
            if not by_sign_data:
                continue

            aspect_name, exact_angle = by_sign_data
            real_distance = angular_distance(p1.longitude, p2.longitude)
            moiety = calculate_moiety(p1.planet, p2.planet)
            phase = classify_aspect_phase(
                p1.planet,
                p1.longitude,
                p2.planet,
                p2.longitude,
                exact_angle,
            )

            is_valid, orb, max_orb = aspect_within_orb(
                real_distance=real_distance,
                exact_angle=exact_angle,
                moiety=moiety,
                phase=phase,
            )
            if not is_valid:
                continue

            aspects.append(
                AspectResult(
                    planet1=p1.planet,
                    planet2=p2.planet,
                    aspect=aspect_name,
                    angle=exact_angle,
                    realDistance=round(real_distance, 2),
                    orb=round(orb, 2),
                    maxOrb=round(max_orb, 2),
                    phase=phase,
                    bySign=True,
                    moiety=round(moiety, 2),
                )
            )

    aspects.sort(key=lambda item: (item.angle, item.orb))
    return [item.to_dict() for item in aspects]


def calculate_chart(
    birth_date: str,
    birth_time: str,
    latitude: float,
    longitude: float,
    tz_name: str = "America/Sao_Paulo",
) -> Dict[str, Any]:
    utc_dt = local_datetime_to_utc(birth_date, birth_time, tz_name)
    jd = utc_datetime_to_julian_day(utc_dt)

    houses, ascmc = swe.houses_ex(jd, latitude, longitude, b"P")
    asc_lon = normalize_angle(ascmc[0])
    mc_lon = normalize_angle(ascmc[1])

    asc_sign, asc_idx, asc_deg = get_sign_and_degree(asc_lon)
    mc_sign, _, mc_deg = get_sign_and_degree(mc_lon)

    positions: List[PlanetPosition] = []
    for planet_name, planet_id in PLANETS.items():
        result, _ = swe.calc_ut(jd, planet_id)
        lon = normalize_angle(result[0])
        speed = result[3]
        positions.append(build_planet_position(planet_name, lon, speed))

    north_node = find_position(positions, "North Node")
    positions.append(build_south_node(north_node))

    sun_pos = find_position(positions, "Sun")
    moon_pos = find_position(positions, "Moon")
    is_day_chart = is_diurnal_chart(asc_lon, sun_pos.longitude)

    positions.append(
        build_part_of_fortune(
            asc_lon=asc_lon,
            sun_lon=sun_pos.longitude,
            moon_lon=moon_pos.longitude,
            is_day_chart=is_day_chart,
        )
    )

    for position in positions:
        position.house = whole_sign_house(position.signIndex, asc_idx)

    dignities = calculate_dignities(
        positions=positions,
        is_day_chart=is_day_chart,
        sun_lon=sun_pos.longitude,
    )
    aspects = calculate_aspects(positions=positions, is_day_chart=is_day_chart)

    return {
        "ascendant": {
            "sign": asc_sign,
            "degree": asc_deg,
            "signIndex": asc_idx,
            "longitude": asc_lon,
        },
        "midheaven": {
            "sign": mc_sign,
            "degree": mc_deg,
            "longitude": mc_lon,
        },
        "isDayChart": is_day_chart,
        "positions": [position.to_dict() for position in positions],
        "dignities": dignities,
        "aspects": aspects,
        "julianDay": jd,
        "utcTime": utc_dt.strftime("%Y-%m-%d %H:%M UTC"),
        "timezone": tz_name,
        "meta": {
            "houseSystemForAngles": "Placidus via Swiss Ephemeris",
            "houseSystemForInterpretation": "Whole Sign",
        },
    }


def calculate_chart_legacy(
    birth_date: str,
    birth_time: str,
    latitude: float,
    longitude: float,
    timezone_value: Any,
) -> Dict[str, Any]:
    if isinstance(timezone_value, str) and "/" in timezone_value:
        tz_name = timezone_value
    elif isinstance(timezone_value, (int, float)):
        offset = int(timezone_value)
        if offset == 0:
            tz_name = "Etc/GMT"
        elif offset > 0:
            tz_name = f"Etc/GMT-{offset}"
        else:
            tz_name = f"Etc/GMT+{abs(offset)}"
    else:
        tz_name = "America/Sao_Paulo"

    return calculate_chart(
        birth_date=birth_date,
        birth_time=birth_time,
        latitude=latitude,
        longitude=longitude,
        tz_name=tz_name,
    )
