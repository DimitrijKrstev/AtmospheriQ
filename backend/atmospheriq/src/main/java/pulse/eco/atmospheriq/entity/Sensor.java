package pulse.eco.atmospheriq.entity;

import jakarta.persistence.*;
import lombok.Data;

import java.util.List;

@Data
@Entity
@Table(name = "sensor")
public class Sensor {
    @Id
    @Column(name = "sensor_id")  // Explicitly define the column name for the sensorId
    private String sensorId;

    @Column(nullable = false)
    private String position;


}
