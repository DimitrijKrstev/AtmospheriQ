package pulse.eco.atmospheriq.entity;

import jakarta.persistence.*;
import lombok.Data;

import java.util.List;

@Data
@Entity
@Table(name = "sensor")
public class Sensor {
    @Id
    private String sensorId;

    @Column(nullable = false)
    private String position;

    @OneToMany(mappedBy = "customer", cascade = CascadeType.ALL)
    private List<Measurement> measurements;

}
