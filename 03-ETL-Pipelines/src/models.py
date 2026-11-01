from pydantic import BaseModel, field_validator, model_validator
from typing import Any, ClassVar, Optional, Sequence
from datetime import datetime

class CurrentWeather(BaseModel):
    cloudCeiling: Optional[float]
    cloudCover: int
    cloudCoverPhrase: str
    dayOfWeek: str
    dayOrNight: str
    expirationTimeUtc: datetime
    iconCode: int
    iconCodeExtend: int
    obsQualifierCode: Optional[int]
    obsQualifierSeverity: Optional[int]
    precip1Hour: float 
    precip6Hour: float 
    precip24Hour: float 
    pressureAltimeter: float 
    pressureChange: float 
    pressureMeanSeaLevel: float 
    pressureTendencyCode: int
    pressureTendencyTrend: str
    relativeHumidity: int
    snow1Hour: float 
    snow6Hour: float 
    snow24Hour: float 
    sunriseTimeLocal: datetime 
    sunriseTimeUtc: datetime 
    sunsetTimeLocal: datetime 
    sunsetTimeUtc: datetime 
    temperature: int 
    temperatureChange24Hour: int 
    temperatureDewPoint: int 
    temperatureFeelsLike: int 
    temperatureHeatIndex: int 
    temperatureMax24Hour: int 
    temperatureMaxSince7Am: int 
    temperatureMin24Hour: int 
    temperatureWetBulbGlobe: int 
    temperatureWindChill: int 
    uvDescription: str 
    uvIndex: int 
    validTimeLocal: datetime 
    validTimeUtc: datetime 
    visibility: float 
    windDirection: int 
    windDirectionCardinal: str 
    windGust: Optional[float] 
    windSpeed: int 
    wxPhraseLong: str 
    wxPhraseMedium: str 
    wxPhraseShort: str
    
class HourlyForecast(BaseModel):
    hour: int
    temperature: int
    temperatureFeelsLike: int
    precipChance: int
    precipRate: float
    windSpeed: int
    windDirectionCardinal: str
    wxPhraseLong: str

class ColumnarForecastModel(BaseModel):
    row_fields: ClassVar[tuple[str, ...]] = ()

    @model_validator(mode="after")
    def ensure_equal_lengths(self):
        if not self.row_fields:
            return self

        lengths = {name: len(getattr(self, name)) for name in self.row_fields}
        unique_lengths = set(lengths.values())
        if len(unique_lengths) != 1:
            raise ValueError(f"All forecast arrays must have equal length. Got: {lengths}")
        return self

    @property
    def periods(self) -> int:
        if not self.row_fields:
            return 0
        return len(getattr(self, self.row_fields[0]))

    def to_rows(self, fields: Sequence[str] | None = None) -> list[dict[str, Any]]:
        selected_fields = tuple(fields) if fields is not None else self.row_fields
        if not selected_fields:
            return []

        rows = []
        for i in range(self.periods):
            rows.append({field: getattr(self, field)[i] for field in selected_fields})
        return rows


class Forecast15Minute(ColumnarForecastModel):
    row_fields: ClassVar[tuple[str, ...]] = (
        "dayOfWeek",
        "iconCode",
        "iconCodeExtend",
        "precipChance",
        "precipRate",
        "precipType",
        "relativeHumidity",
        "snowRate",
        "temperature",
        "temperatureFeelsLike",
        "validTimeLocal",
        "windDirection",
        "windDirectionCardinal",
        "windSpeed",
        "wxPhraseLong",
        "wxPhraseShort",
        "wxSeverity",
    )

    dayOfWeek: list[str]
    iconCode: list[int]
    iconCodeExtend: list[int]
    precipChance: list[int]
    precipRate: list[float]
    precipType: list[str]
    relativeHumidity: list[int]
    snowRate: list[float]
    temperature: list[int]
    temperatureFeelsLike: list[int]
    validTimeLocal: list[datetime]
    windDirection: list[int]
    windDirectionCardinal: list[str]
    windSpeed: list[int]
    wxPhraseLong: list[str]
    wxPhraseShort: list[str]
    wxSeverity: list[int]


class Forecast2DayHourly(ColumnarForecastModel):
    row_fields: ClassVar[tuple[str, ...]] = (
        "cloudCover",
        "dayOfWeek",
        "dayOrNight",
        "expirationTimeUtc",
        "iconCode",
        "iconCodeExtend",
        "precipChance",
        "precipType",
        "pressureMeanSeaLevel",
        "qpf",
        "qpfIce",
        "qpfRain",
        "qpfSnow",
        "relativeHumidity",
        "stormId",
        "temperature",
        "temperatureDewPoint",
        "temperatureFeelsLike",
        "temperatureHeatIndex",
        "temperatureWindChill",
        "uvDescription",
        "uvIndex",
        "validTimeLocal",
        "validTimeUtc",
        "visibility",
        "windDirection",
        "windDirectionCardinal",
        "windGust",
        "windSpeed",
        "wxPhraseLong",
        "wxPhraseShort",
        "wxSeverity",
    )

    cloudCover: list[int]
    dayOfWeek: list[str]
    dayOrNight: list[str]
    expirationTimeUtc: list[int]
    iconCode: list[int]
    iconCodeExtend: list[int]
    precipChance: list[int]
    precipType: list[str]
    pressureMeanSeaLevel: list[float]
    qpf: list[float]
    qpfIce: list[float]
    qpfRain: list[float]
    qpfSnow: list[float]
    relativeHumidity: list[int]
    stormId: list[Optional[str]]
    temperature: list[int]
    temperatureDewPoint: list[int]
    temperatureFeelsLike: list[int]
    temperatureHeatIndex: list[int]
    temperatureWindChill: list[int]
    uvDescription: list[str]
    uvIndex: list[int]
    validTimeLocal: list[datetime]
    validTimeUtc: list[int]
    visibility: list[float]
    windDirection: list[int]
    windDirectionCardinal: list[str]
    windGust: list[Optional[int]]
    windSpeed: list[int]
    wxPhraseLong: list[str]
    wxPhraseShort: list[str]
    wxSeverity: list[int]


class ForecastDaypart(ColumnarForecastModel):
    row_fields: ClassVar[tuple[str, ...]] = (
        "cloudCover",
        "dayOrNight",
        "daypartName",
        "iconCode",
        "iconCodeExtend",
        "narrative",
        "precipChance",
        "precipType",
        "qpf",
        "qpfIce",
        "qpfRain",
        "qpfSnow",
        "qualifierCode",
        "qualifierPhrase",
        "relativeHumidity",
        "snowRange",
        "temperature",
        "temperatureHeatIndex",
        "temperatureWindChill",
        "thunderCategory",
        "thunderIndex",
        "uvDescription",
        "uvIndex",
        "windDirection",
        "windDirectionCardinal",
        "windPhrase",
        "windSpeed",
        "wxPhraseLong",
        "wxPhraseShort",
    )

    cloudCover: list[int]
    dayOrNight: list[str]
    daypartName: list[str]
    iconCode: list[int]
    iconCodeExtend: list[int]
    narrative: list[str]
    precipChance: list[int]
    precipType: list[str]
    qpf: list[float]
    qpfIce: list[float]
    qpfRain: list[float]
    qpfSnow: list[float]
    qualifierCode: list[Optional[str]]
    qualifierPhrase: list[Optional[str]]
    relativeHumidity: list[int]
    snowRange: list[str]
    temperature: list[int]
    temperatureHeatIndex: list[int]
    temperatureWindChill: list[int]
    thunderCategory: list[str]
    thunderIndex: list[int]
    uvDescription: list[str]
    uvIndex: list[int]
    windDirection: list[int]
    windDirectionCardinal: list[str]
    windPhrase: list[str]
    windSpeed: list[int]
    wxPhraseLong: list[str]
    wxPhraseShort: list[str]


class DailyForecastBase(ColumnarForecastModel):
    row_fields: ClassVar[tuple[str, ...]] = (
        "calendarDayTemperatureMax",
        "calendarDayTemperatureMin",
        "dayOfWeek",
        "expirationTimeUtc",
        "moonPhase",
        "moonPhaseCode",
        "moonPhaseDay",
        "moonriseTimeLocal",
        "moonriseTimeUtc",
        "moonsetTimeLocal",
        "moonsetTimeUtc",
        "narrative",
        "qpf",
        "qpfIce",
        "qpfRain",
        "qpfSnow",
        "sunriseTimeLocal",
        "sunriseTimeUtc",
        "sunsetTimeLocal",
        "sunsetTimeUtc",
        "temperatureMax",
        "temperatureMin",
        "validTimeLocal",
        "validTimeUtc",
    )

    calendarDayTemperatureMax: list[int]
    calendarDayTemperatureMin: list[int]
    dayOfWeek: list[str]
    expirationTimeUtc: list[int]
    moonPhase: list[str]
    moonPhaseCode: list[str]
    moonPhaseDay: list[int]
    moonriseTimeLocal: list[Optional[datetime]]
    moonriseTimeUtc: list[Optional[int]]
    moonsetTimeLocal: list[datetime]
    moonsetTimeUtc: list[int]
    narrative: list[str]
    qpf: list[float]
    qpfIce: list[float]
    qpfRain: list[float]
    qpfSnow: list[float]
    sunriseTimeLocal: list[datetime]
    sunriseTimeUtc: list[int]
    sunsetTimeLocal: list[datetime]
    sunsetTimeUtc: list[int]
    temperatureMax: list[int]
    temperatureMin: list[int]
    validTimeLocal: list[datetime]
    validTimeUtc: list[int]
    daypart: list[ForecastDaypart]

    @field_validator("moonriseTimeLocal", mode="before")
    @classmethod
    def normalize_optional_moonrise_datetimes(cls, value):
        if isinstance(value, list):
            return [None if item == "" else item for item in value]
        return value


class Forecast3DayDaily(DailyForecastBase):
    pass


class Forecast7DayDaily(DailyForecastBase):
    pass


def to_rows(forecast: ColumnarForecastModel, fields: Sequence[str] | None = None) -> list[dict[str, Any]]:
    return forecast.to_rows(fields)