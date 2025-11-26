namespace API.Dtos;

public class PredictIn
{
    public float Bedrooms { get; set; }
    public float Bathrooms { get; set; }
    public float Sqm { get; set; }

    public string City { get; set; } = string.Empty;
}
