# City and State Differentiation Fix Plan

## Current Issue Analysis
After analyzing the codebase, I found that while the forms correctly differentiate between city and state as separate fields, the database models store them as a combined address field. This creates several problems:

1. **Forms**: City and state are properly separated with distinct choices and validation
2. **Database**: Only a single `address` field exists in both patient and doctor models
3. **Data Loss**: City and state information gets concatenated into one string, making it impossible to query or filter by city/state separately

## Proposed Solution

### 1. Database Schema Updates
- Add separate `city` and `state` fields to patient and doctor models
- Keep existing `address` field for street address
- Create migration for schema changes

### 2. Form Updates
- Update forms to properly separate city, state, and street address
- Ensure validation works correctly for the new field structure

### 3. View Updates
- Update signup views to handle the new field structure
- Update profile views to work with separated fields

### 4. Template Updates
- Update templates to display and handle the new field structure
- Ensure proper validation and user experience

### 5. Data Migration
- Create script to migrate existing data from combined address to new fields
- Handle cases where address parsing might be needed

## Implementation Steps

### Step 1: Update Database Models
- [ ] Add city and state fields to patient model
- [ ] Add city and state fields to doctor model  
- [ ] Create migration files

### Step 2: Update Forms
- [ ] Modify PatientSignupForm to use separate fields
- [ ] Modify DoctorSignupForm to use separate fields
- [ ] Update validation logic

### Step 3: Update Views
- [ ] Update patient signup view
- [ ] Update doctor signup view
- [ ] Update profile update views
- [ ] Update any other views that handle address

### Step 4: Update Templates
- [ ] Update patient signup template
- [ ] Update doctor signup template
- [ ] Update profile templates
- [ ] Update any other address-related templates

### Step 5: Data Migration
- [ ] Create data migration script
- [ ] Test migration on sample data
- [ ] Run migration in production

### Step 6: Testing
- [ ] Test signup flows
- [ ] Test profile updates
- [ ] Test data consistency
- [ ] Test address display throughout the system

### Step 7: Cleanup
- [ ] Remove any deprecated code
- [ ] Update documentation
- [ ] Final validation

## Expected Benefits

1. **Proper Data Separation**: City and state will be stored as distinct, searchable fields
2. **Better Querying**: Ability to filter users by city or state
3. **Improved User Experience**: Users can update location information more precisely
4. **Data Integrity**: Clear separation prevents data corruption
5. **Scalability**: System can handle more complex location-based features in the future

## Technical Considerations

1. **Backward Compatibility**: Existing data will be migrated properly
2. **Validation**: Ensure proper validation for the new field structure
3. **Performance**: New fields should be indexed for efficient querying
4. **User Interface**: Update all templates to work with the new structure
