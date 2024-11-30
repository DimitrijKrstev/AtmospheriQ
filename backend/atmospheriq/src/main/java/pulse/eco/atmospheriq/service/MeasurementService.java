package pulse.eco.atmospheriq.service;

import lombok.AllArgsConstructor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Service;
import pulse.eco.atmospheriq.entity.Measurement;
import pulse.eco.atmospheriq.kafka.KafkaProducerService;
import pulse.eco.atmospheriq.repository.MeasurementRepo;
import pulse.eco.atmospheriq.repository.SensorRepo;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@AllArgsConstructor
public class MeasurementService {
    private final MeasurementRepo measurementRepo;
    private final KafkaProducerService kafkaProducerService;

    public void saveMeasurements(List<Measurement> measurements) {
        List<Measurement> currentMeasurements = getAllMeasurements();
        for (Measurement measurement : measurements){
            Optional<Measurement> existent = currentMeasurements.stream().filter((x) ->
                            x.getSensorId().equals(measurement.getSensorId()) && x.getType().equals(measurement.getType()))
                    .findFirst();

            if (existent.isPresent()){
                Measurement updated = existent.get();
                if (updated.getStamp().equals(measurement.getStamp())) continue;

                updated.setValue(measurement.getValue());
                updated.setStamp(measurement.getStamp());
                measurementRepo.save(updated);
            }
            else{
                measurementRepo.save(measurement);
            }

            kafkaProducerService.sendMeasurement(measurement);
        }
    }

    public List<Measurement> getAllMeasurements(){
        return measurementRepo.findAll();
    }

    public Measurement findById(Long id){
        return measurementRepo.findById(id).get();
    }

    public List<Measurement> findAllBySensor(String id){
        return measurementRepo.findAll()
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
                    LocalDateTime timestamp1 = LocalDateTime.parse(m1.getStamp(), formatter);
                    LocalDateTime timestamp2 = LocalDateTime.parse(m2.getStamp(), formatter);
                    return timestamp2.compareTo(timestamp1);
                })
                .limit(3)
                .collect(Collectors.toList());
    }

}
