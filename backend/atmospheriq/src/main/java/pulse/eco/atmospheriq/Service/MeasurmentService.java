package pulse.eco.atmospheriq.Service;

import org.springframework.stereotype.Service;
import pulse.eco.atmospheriq.entity.Measurement;
import pulse.eco.atmospheriq.repository.MeasurmentRepo;
import pulse.eco.atmospheriq.repository.SensorRepo;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class MeasurmentService {
    private final MeasurmentRepo measurmentRepo;

    public MeasurmentService(MeasurmentRepo measurmentRepo, SensorRepo sensorRepo) {
        this.measurmentRepo = measurmentRepo;
    }
    public List<Measurement> getAll(){
        return measurmentRepo.findAll();
    }
    public Measurement findById(Long id){
        return measurmentRepo.findById(id).get();
    }
    public List<Measurement> findBySensor(String id){
        return measurmentRepo.findAll()
                .stream().filter(x->x.getSensorId().equals(id))
                .collect(Collectors.toList());
    }
    public List<Measurement> findAllbyType(List<Measurement>measurements,String type){
        return measurements
                .stream()
                .filter(x->x.getType().equals(type))
                .collect(Collectors.toList());
    }
    public static List<Measurement> getLatestMeasurements(List<Measurement> measurements) {
        DateTimeFormatter formatter = DateTimeFormatter.ISO_DATE_TIME;

        return measurements.stream()
                .sorted((m1, m2) -> {
                    LocalDateTime timestamp1 = LocalDateTime.parse(m1.getTimestamp(), formatter);
                    LocalDateTime timestamp2 = LocalDateTime.parse(m2.getTimestamp(), formatter);
                    return timestamp2.compareTo(timestamp1);
                })
                .limit(3)
                .collect(Collectors.toList());
    }

}
