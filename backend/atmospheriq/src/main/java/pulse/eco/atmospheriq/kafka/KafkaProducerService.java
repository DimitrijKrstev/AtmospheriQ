package pulse.eco.atmospheriq.kafka;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import pulse.eco.atmospheriq.entity.Measurement;

@Service
public class KafkaProducerService {

    private final KafkaTemplate<String, Measurement> kafkaTemplate;

    @Value("${kafka.topic.measurements}")
    private String topic;

    public KafkaProducerService(KafkaTemplate<String, Measurement> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void sendMeasurement(Measurement measurement) {
        kafkaTemplate.send(topic, measurement);
    }
}

