package pulse.eco.atmospheriq.service;

import org.springframework.stereotype.Service;
import pulse.eco.atmospheriq.entity.Sensor;
import pulse.eco.atmospheriq.repository.SensorRepo;

import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class SensorService {
private  final SensorRepo sensorRepo;

    public SensorService(SensorRepo sensorRepo) {
        this.sensorRepo = sensorRepo;
    }

    public List<Sensor> getAll(){
        return sensorRepo.findAll();
    }

    public Sensor findById(String id){
        return sensorRepo.findById(id).get();
    }

    public static double haversine(double lat1, double lon1, double lat2, double lon2) {
        final int EARTH_RADIUS_KM = 6371;

        double dLat = Math.toRadians(lat2 - lat1);
        double dLon = Math.toRadians(lon2 - lon1);

        double a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2)) *
                        Math.sin(dLon / 2) * Math.sin(dLon / 2);

        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return EARTH_RADIUS_KM * c;
    }

    public  List<Sensor> findNearestSensors(String id) {

        String[] targetCoords = sensorRepo.findById(id).get().getPosition().split(",");
        double targetLat = Double.parseDouble(targetCoords[0].trim());
        double targetLon = Double.parseDouble(targetCoords[1].trim());

        return sensorRepo.findAll().stream()
                .sorted(Comparator.comparingDouble(sensor -> {
                    String[] positionCoords = sensor.getPosition().split(",");
                    double sensorLat = Double.parseDouble(positionCoords[0].trim());
                    double sensorLon = Double.parseDouble(positionCoords[1].trim());
                    return haversine(targetLat, targetLon, sensorLat, sensorLon);
                }))
                .limit(3)
                .collect(Collectors.toList());
    }
}
